<script>
	import { resolveRoute } from "$app/paths";
    import PieChartTonality from "./PieChartTonality.svelte";

    let { resultData, topic, resolvedTopic } = $props()

    let numbers = $state(null);

    $effect(() => {
        if (resultData) {
            numbers =  [
                { tone: "positive", percentage: resultData?.positive ?? 0 },
                { tone: "neutral",  percentage: resultData?.neutral  ?? 0 },
                { tone: "negative", percentage: resultData?.negative ?? 0 }
            ]
    }});

  /*let numbers = [
        { tone: "positive", percentage: 10 },
        { tone: "neutral", percentage: 50 },
        { tone: "negative", percentage: 40 }
  ];*/
  

</script>

<section>
    {#if numbers && (resultData.positive > 0 || resultData.neutral > 0 || resultData.negative > 0)}
    <h3>Verteilung der Stimmung</h3>
    <PieChartTonality 
        data={numbers} 
        {topic} 
        {resolvedTopic}/>
    {/if}
</section>
