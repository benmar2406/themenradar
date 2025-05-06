<script>

let { summary } = $props();

</script>

<div class="summary-container item-container">
    <h3 class="part-title">Key Facts</h3>
    <div class="summaries">
        <div>
            <p class="summary-title">Artikel gefunden:</p>
            <p class="summary-number">{summary?.total}</p>
        </div>
        <div>
            <p class="summary-title">Davon positiv:</p>
            <p class="summary-number">{summary?.positive}</p>
        </div>
        <div>
            <p class="summary-title">Davon neutral:</p>
            <p class="summary-number">{summary?.neutral}</p>
        </div>
        <div>
            <p class="summary-title">Davon negativ:</p>
            <p class="summary-number">{summary?.negative}</p>
        </div>
    </div>
    <p class="dominant-sentiment">Überwiegendes Sentiment: {summary.dominantSentiment}</p>
</div>

<style> 


    .summaries {
        display: flex;
        flex-wrap: wrap;
        margin-top: 4rem;
    }

    .summaries > div {
        flex-basis: 47%;
        gap: 1rem;
        background-color: #FFF01C;
        padding: 0.7rem;
        margin: 0.4rem;
        box-sizing: border-box;
        border-radius: 10px;
        height: 7rem;
    }

    .summary-title, .summary-number {
        padding: 0.5rem;
    }

    .summary-title {
        padding-bottom: 0.2rem;
        margin-bottom: 0.2rem; 
        margin-top: 0.2rem;
    }

    .summary-number {
        font-weight: 600;
        font-size: 1.8rem;
        padding-top: 0.2rem;
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
    }

    .dominant-sentiment {
        padding-top: 0.2rem;
        margin-top: 0.2rem;
        padding: 1.2rem;
        font-weight: 600;

    }
    


</style>
