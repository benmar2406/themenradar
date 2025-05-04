<script>
	import { resolveRoute } from "$app/paths";
    import PieChartTonality from "./PieChartTonality.svelte";
    import Summary from "../Summary.svelte";
    import TopArticle from "../TopArticle.svelte";

    let { resultData } = $props()

    /*let numbers = $state(null);

    $effect(() => {
        if (resultData) {
            numbers =  [
                { tone: "positive", percentage: resultData?.positive ?? 0 },
                { tone: "neutral",  percentage: resultData?.neutral  ?? 0 },
                { tone: "negative", percentage: resultData?.negative ?? 0 }
            ]
    }});*/

//mockup data for testing
  const numbers = [
        { tone: "positive", percentage: 20 },
        { tone: "neutral", percentage: 30 },
        { tone: "negative", percentage: 50 }
  ];

  let topic = 'Klimmawandel';
  let resolvedTopic = 'Klimawandel Test'

  const summary = {
            "positive": 20,
            "neutral": 30,
            "negative": 50,
            "total": 100,
            "dominantSentiment": 'negativ'
        }

    let results = [{
            "article": {
                "title": "Deggendorfer Stadtgärtnerei: Grüner Daumen trotz Klimawandel. Was macht der Klimawandel mit dem Wetter?",
                "source": "Golem",
                "url": "https://www.golem.de/news/klimawandelsimulation-dubai-am-rhein-2505-195460.html",
                "content": "Durch den Klimawandel treten Wetterextreme wie Dürren viel öfter auf. Ein Simulationswerkzeug zeigt, welchen Einfluss das lokal haben kann."
            },
            "analysis": "negative"
        }]
  

</script>

<section>
    <div class="bg">
        <h2 class='results-title'>Deine Auswertung zum Thema »{resolvedTopic}«</h2>
    </div>
    <!--{#if numbers && (resultData.positive > 0 || resultData.neutral > 0 || resultData.negative > 0)}
    <PieChartTonality 
        data={numbers} 
        {topic} 
        {resolvedTopic}>
    {/if}-->
    <div class="results-visualization">
        <Summary {summary}/>
        <PieChartTonality 
            data={numbers} 
            {topic} 
            {resolvedTopic}/>
        <TopArticle {results}/>
        
    </div>
</section>

<style>
    section {
        margin: 4rem auto;
        width: 80%;
        padding: 0rem;
        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
        border-radius: 20px;
    }

    .results-visualization {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }

    .bg {
        background-color: #fff01c;
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
    }

    .results-title {
        text-align: center;
        padding: 2rem;
        padding-bottom: 2rem;
        margin: 0;
    }

    
</style>