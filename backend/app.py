"""
Flask backend
─────────────
/analyze          → sentiment of arbitrary text
/analyze-media    →   • historical sentiment by month   (monthly_percentages, results)
                     • current 30-day pulse             (summary_recent, mostRecentArticle)
"""
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import os
import traceback
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline

# ────────────────────────── config ──────────────────────────
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

classifier    = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
BASE_URL      = "https://gnews.io/api/v4/search"

# ──────────────────────── helpers ──────────────────────────
def run_topic_sentiment_analysis(topic: str, text: str) -> dict:
    """Zero-shot classify text as positive / neutral / negative about <topic>."""
    if not topic or not text:
        raise ValueError("Missing topic or text")
    labels = [
        f"positive about {topic}",
        f"neutral toward {topic}",
        f"negative about {topic}",
    ]
    res = classifier(text, candidate_labels=labels, multi_label=False)
    return {
        "labels":   res["labels"],
        "scores":   res["scores"],
        "sequence": res["sequence"],
        "topLabel": res["labels"][0],
    }


def parse_iso(ts: str) -> datetime:
    """RFC 3339 → aware UTC datetime."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def pct(part: int, whole: int) -> float:
    return round((part / whole) * 100, 2) if whole else 0.0


def pct_dict(counts: dict) -> dict:
    total = sum(counts.values())
    return {k: pct(v, total) for k, v in counts.items()} if total else {k: 0.0 for k in counts}

# ─────────────────────── routes ────────────────────────────
@app.route("/analyze", methods=["POST"])
def analyze_topic_sentiment():
    try:
        data  = request.get_json(force=True)
        topic = data.get("topic", "").strip()
        text  = data.get("text", "").strip()
        return jsonify(run_topic_sentiment_analysis(topic, text))
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/analyze-media", methods=["POST"])
def analyze_media():
    try:
        data  = request.get_json(force=True)
        topic = (data.get("topic") or "").strip()
        if not topic:
            return jsonify({"error": "Missing topic"}), 400

        # ────────────────── 1) historical set (sort=relevance) ──────────────────
        three_years_back = (datetime.now(timezone.utc) - timedelta(days=3*365)).strftime("%Y-%m-%d")
        
        params_relevance = {
            "q": topic,
            "lang": "de",
            "max": 100,           # GNews upper limit
            "sort": "relevance",
            "from":  three_years_back,
            "token": GNEWS_API_KEY,
        }
        rel_resp = requests.get(BASE_URL, params=params_relevance)
        if rel_resp.status_code == 403:
            return jsonify({"error": "API limit reached"}), 429
        rel_articles = rel_resp.json().get("articles", [])
        if not rel_articles:
            return jsonify({"error": "No articles found for this topic"}), 404

        month_buckets = defaultdict(
            lambda: {"positive": 0, "neutral": 0, "negative": 0, "total": 0}
        )
        results = []

        for art in rel_articles:
            content = art.get("description") or art.get("content") or ""
            if not content.strip():
                continue

            analysis   = run_topic_sentiment_analysis(topic, content)
            label_root = analysis["topLabel"].split()[0].lower()   # positive | neutral | negative

            pub_dt   = parse_iso(art.get("publishedAt", "1970-01-01T00:00:00Z"))
            mkey     = pub_dt.strftime("%Y-%m")
            month_buckets[mkey]["total"]      += 1
            month_buckets[mkey][label_root]   += 1

            results.append(
                {
                    "article": {
                        "title":         art.get("title", ""),
                        "source":        art.get("source", {}).get("name", ""),
                        "url":           art.get("url", ""),
                        "publishedDate": art.get("publishedAt", ""),
                        "content":       content,
                    },
                    "analysis": analysis,
                }
            )

        monthly_percentages = {}
        for month, counts in month_buckets.items():
            total = counts.pop("total")
            monthly_percentages[month] = pct_dict(counts)

        # ────────────────── 2) current set (sort=publishedAt) ──────────────────
        params_latest = {
            "q": topic,
            "lang": "de",
            "max": 100,
            "sort": "publishedAt",
            "token": GNEWS_API_KEY,
        }
        latest_resp = requests.get(BASE_URL, params=params_latest)
        if latest_resp.status_code == 403:
            return jsonify({"error": "API limit reached"}), 429
        latest_articles = latest_resp.json().get("articles", [])
        if not latest_articles:
            return jsonify({"error": "No recent articles found"}), 404

        recent_window = datetime.now(timezone.utc) - timedelta(days=30)
        recent_counts = {"positive": 0, "neutral": 0, "negative": 0}

        newest_art      = latest_articles[0]
        newest_content  = newest_art.get("description") or newest_art.get("content") or ""
        newest_analysis = run_topic_sentiment_analysis(topic, newest_content)

        for art in latest_articles:
            content     = art.get("description") or art.get("content") or ""
            if not content.strip():
                continue

            label_root  = run_topic_sentiment_analysis(topic, content)["topLabel"].split()[0].lower()
            pub_dt      = parse_iso(art.get("publishedAt", "1970-01-01T00:00:00Z"))
            if pub_dt >= recent_window:
                recent_counts[label_root] += 1

        summary_recent = {
            **recent_counts,
            "percentages": pct_dict(recent_counts),
            "total":       sum(recent_counts.values()),
            "dominantSentiment": max(recent_counts, key=recent_counts.get)
                                 if sum(recent_counts.values()) else None,
            "windowDays": 30,
        }

        most_recent_article = {
            "article": {
                "title":         newest_art.get("title", ""),
                "source":        newest_art.get("source", {}).get("name", ""),
                "url":           newest_art.get("url", ""),
                "publishedDate": newest_art.get("publishedAt", ""),
                "content":       newest_content,
            },
            "analysis": newest_analysis,
        }

        # ───────────────────── response ──────────────────────────────
        return jsonify(
            {
                "summary_recent":      summary_recent,      # 30-day snapshot
                "monthly_percentages": monthly_percentages, # historical trend
                "results":             results,             # per-article list
                "mostRecentArticle":   most_recent_article, # newest headline
            }
        )

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ───────────────────────── main ─────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
