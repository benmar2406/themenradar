<script>

    import { SvelteDate } from 'svelte/reactivity';

    let { topArticle  } = $props();

    let publishedDate = new SvelteDate(topArticle.article.publishedAt).toLocaleDateString("de-DE");
    let topLabel = $state(topArticle.analysis.topLabel.split(' ')[0]);
    let tonality = $state('')
    
    $effect(() => {
        switch (topLabel) {
            case 'positive':
                tonality = 'positiv';
                break;
            case 'neutral':
                tonality = 'neutral';
                break;
            case 'negative':
                tonality = 'negativ';
                break;
            default:
            tonality = 'keine Tonalität ermittelt';
        } 
    })

</script>

<div class="item-container">
    <h3 class="part-title">Relevantester Artikel zum Thema</h3>
    <div>
        <p><span>Titel:</span> {topArticle.article.title}</p>
        <p><span>Medium:</span> {topArticle.article.source.name}</p>
        <p><span>Veröffentlichung:</span> {publishedDate}</p>
        <a 
            href={topArticle.article.url} 
            target="_blank">
            <button>
                Zum Artikel
            </button>
        </a>
        <p><span>Sentiment:</span> {tonality}</p>
    </div>
</div>

<style> 
    span {
        font-weight: 600;   
    }

    @media only screen and (max-width: 1000px) {
    .item-container {
      margin: 3rem auto;
      width: 85%;
    }
  }

</style>
