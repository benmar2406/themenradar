<script>
    import Form from "./Form.svelte";
    import { fade } from 'svelte/transition';
    let { 
        analyze,
        topic = $bindable(),
        text,
        error,
        loading,
        ownTextSelected,
        newsSelected,
        route,
        result
    } = $props()
    
    let selectedIndex = $state(null);
    const buttons = ["Eigenen Artikel", "Medienanalyse"]
    
    
    const handleButtonClick = (index) => {

        selectedIndex = index;

        if (index === 0) {
            ownTextSelected = true;
            newsSelected = false;
            route = 'analyze'
        } else if (index === 1) {
            newsSelected = true;
            ownTextSelected = false;
            route = 'analyze-media'
        }
    }

</script>

    <div class="form-container">
        <h2>Selbst Artikel eingeben oder Medien analysieren</h2>
        <div class="button-container">
            {#each buttons as button, index}
                <button 
                    onclick={() => handleButtonClick(index)}
                    class:selected={index === selectedIndex}
                    >{button}
                </button>
            {/each}
        </div>
        {#if newsSelected === true || ownTextSelected === true}
        <div>
            <Form 
                {analyze} 
                bind:topic={topic} 
                {text}
                {loading}
                {ownTextSelected}
                {newsSelected}
                {route}
            />
            <div>
                {#if loading}
                    <p>Analysiere, das kann eine Weile dauern...</p>
                {/if}
        
                {#if error}
                    {#if error.message === 'No articles found for this topic'}
                        <p>Keine Artikel zum Thema gefunden, versuche es mit einem anderen Begriff.</p>
                    {:else}
                        <p>Fehler: {error.message}</p>
                    {/if}
                {/if}
            </div>
        
        </div>
    {/if}
    </div>
<style>
    .form-container {
        width: 40vw;
        padding: 2rem;
        display: block;
    }

    .button-container {
        display: flex;
        width: 90%;
        margin-bottom: 2rem;
        padding: 0.3rem;
        align-items: center;
    }

    .button-container button {
        font-size: 1.1rem;
        margin-right: 2rem;
    }
</style>
