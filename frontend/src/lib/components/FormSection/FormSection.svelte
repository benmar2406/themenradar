<script>
    import FormContainer from "./Form/FormContainer.svelte";

    let { 
        analyze,
        topic = $bindable(),
        text,
        error,
        loading,
        ownTextSelected,
        newsSelected,
        route,
        result,
    } = $props()

</script>

<section class="form-section">
    <FormContainer 
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
    <article>
        <h3>Anleitung und Tips</h3>
        <ul>
            <li><strong>Einzelne Begriffe verwenden:</strong> Gib klare, spezifische Themen ein, z. B. „Künstliche Intelligenz“ oder „Klimaschutz“.</li>
            <li><strong>Keine Fragen formulieren:</strong> Vermeide vollständige Sätze oder Fragen; kurze Stichwörter liefern bessere Ergebnisse.</li> 
            <li><strong>Aktuelle Themen wählen:</strong> Wähle Themen, die derzeit in den Medien präsent sind, um relevante Artikel zu erhalten.</li> 
            <li><strong>Begriffskombinationen nutzen:</strong> Kombiniere verwandte Begriffe wie „Elektromobilität“ und „Batterietechnologie“ für spezifischere Analysen.</li> 
        </ul>
    </article>
</section>

<style>
    .form-section {
        display: flex;
    }

    .form-section article {
        flex-basis: 40%;
    }

    li {
        padding-bottom: 1.5rem;
    }

</style>