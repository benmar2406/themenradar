<script>
    import ResultsVisualization from "../ResultsVisualization/Charts/ResultsVisualization.svelte";
    import FormSection from "../FormSection/FormSection.svelte";

    let topic = $state('Thema');
    let resolvedTopic = $state('')
    let text = $state('');
    let error = $state(null);
    let loading = $state(false);
    let tonality = $state('');
    let route = $state('');
    let result = $state(null);
    let newsSelected = $state(false);
    let ownTextSelected = $state(false);
    let resultData = $state(null);
    let statusOk =  $state(false);

    async function analyze(topic, text, route) {
        loading = true;
        error = null;
        
        try {
            const payload = { topic };
            if (ownTextSelected) {
                payload.text = text;
            }

            const res = await fetch(`http://localhost:5000/${route}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                result = data;
                console.log(result);
                statusOk = true;

            } else {

                if (res.status === '404') {
                    throw new Error(data.error || 'Fehler: Es wurden keine Artikel gefunden.');
                } else {
                    throw new Error(data.error || 'Ein Fehler ist aufgetreten.');
                }
            }

            console.log(statusOk)

        } catch (err) {
            error = err;

        } finally {
            loading = false;
            if (statusOk) {
                resolvedTopic = topic
            } 
        }
    }
</script>
<FormSection
    {analyze}
    bind:topic={topic}
    {text}
    {error}
    {loading}
    {ownTextSelected}
    {newsSelected}
    {route}
    {result}
    />
<ResultsVisualization 
    resultData={result} 
    {resolvedTopic}
    bind:topic={topic}
    />
