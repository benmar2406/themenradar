from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import traceback
import requests


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def run_topic_sentiment_analysis(topic, text):
    if not topic or not text:
        raise ValueError("Missing topic or text")

    candidate_labels = [
        f"positive about {topic}",
        f"neutral toward {topic}",
        f"negative about {topic}"
    ]

    result = classifier(text, candidate_labels=candidate_labels, multi_label=False)

    return {
        "labels": result["labels"],
        "scores": result["scores"],
        "sequence": result["sequence"],
        "topLabel": result["labels"][0],
    }


@app.route('/analyze', methods=['POST'])
def analyze_topic_sentiment():
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        text = data.get('text', '').strip()
        analysis = run_topic_sentiment_analysis(topic, text)
        
        return jsonify(analysis)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500



GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

@app.route('/analyze-media', methods=['POST'])
def analyze_media():
    try:
        data = request.get_json()
        topic = (data.get('topic') or '').strip()
        if not topic:
            return jsonify({"error": "Missing topic"}), 400

        # GNews API request
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": topic,
            "lang": "de",
            "max": 50,
            "sort": "relevance",
            "token": GNEWS_API_KEY
        }

        response = requests.get(url, params=params)
        articles = response.json().get("articles", [])

        if response.status_code == 403:
            return jsonify({"error": "API limit reached"}), 429 

        articles = response.json().get("articles", [])
        if not articles:
            return jsonify({"No articles found for this topic"}), 404

        results = []
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

        for article in articles:
            content = article.get("description") or article.get("content") or ""
            if not content.strip():
                continue

            analysis = run_topic_sentiment_analysis(topic, content)
            label = analysis["topLabel"].lower()
            if "positive" in label:
                sentiment_counts["positive"] += 1
            elif "neutral" in label:
                sentiment_counts["neutral"] += 1
            elif "negative" in label:
                sentiment_counts["negative"] += 1

            results.append({
                "article": {
                    "title": article.get("title", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "url": article.get("url", ""),
                    "content": content
                },
                "analysis": analysis
            })

        total = sum(sentiment_counts.values())
        dominant = max(sentiment_counts, key=sentiment_counts.get)
        
        percentages = {
            "positive": round((sentiment_counts["positive"] / total) * 100, 2),
            "neutral": round((sentiment_counts["neutral"] / total) * 100, 2),
            "negative": round((sentiment_counts["negative"] / total) * 100, 2)
        }

        summary = {
            "positive": sentiment_counts["positive"],
            "neutral": sentiment_counts["neutral"],
            "negative": sentiment_counts["negative"],
            "percentages": percentages,
            "total": total,
            "dominantSentiment": dominant
        }
        
        print(summary)

        return jsonify({
            "summary": summary,
            "results": results
        })

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
