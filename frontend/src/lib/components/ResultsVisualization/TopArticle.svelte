<script>

    let { summary, results  } = $props();

</script>

<div class="item-container">
    <h3 class="part-title">Relevantester Artikel zum Thema</h3>
    <div>
        <p><span>Titel:</span> {results[0].article.title}</p>
        <p><span>Medium:</span> {results[0].article.source}</p>

        <a href={results[0].article.url} target="_blank"><button>Zum Artikel</button></a>
    </div>
</div>

<style> 
    span {
        font-weight: 600;
    }

</style>
