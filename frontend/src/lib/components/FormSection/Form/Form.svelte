<script>
    import Spinner from "../../Spinner/Spinner.svelte";
    import { fade } from "svelte/transition";
    import { topic } from "../../shared"

    let { analyze, text, loading, ownTextSelected, newsSelected, route } = $props();


    function handleSubmit(event) {
        event.preventDefault();
        analyze($topic, text, route); 
  }


  let readyToSubmit = $state(false)

    $effect(() => {
        if ((ownTextSelected && $topic.trim().length > 0 && text.trim().length > 0) || (newsSelected && $topic.trim().length > 0)) {
            readyToSubmit = true;
        } else {
            readyToSubmit = false;
        }
    });

</script>

<form onsubmit={handleSubmit}>
    <label for="topic">Gebe dein Thema ein:</label><br>
    <input bind:value={$topic} type="text" id="topic" name="topic"><br>
    {#if ownTextSelected}
        <textarea 
            bind:value={text} 
            transition:fade
            placeholder="Gebe einen Text über das Thema ein." 
            type="text" 
            id="text" 
            name="text" 
            rows="8" 
            cols="100">
        </textarea><br>
    {/if}
    
    {#if readyToSubmit}
        <button>    
            {#if loading}
                <Spinner />
            {/if}
            <span>Analysieren</span>
        </button>
    {/if}
</form>

<style>
    form {
        width: 100%;
    }
   
    input, textarea {
        margin: 1rem 0;
        padding: 1rem;
        width: 100%;
        height: 3rem;
        border-radius: 20px;
        border: solid 2px black;
        box-sizing: border-box;
        font-family: 'Poppins';
        font-weight: 400;
    }

    #topic {
       width: 50%;
    }

    #text {
        width: 100%;
        height: 100%;
        resize: none;
    }

    label {
        text-align: center;
    }

    @media only screen and (max-width: 1150px) {
        
        form {
            margin: 4rem auto;
            display: flex;
            flex-direction: column;
            justify-items: flex-start;
            justify-content: flex-start;
        }

        input, textarea {
            margin: 0.5rem auto;
            height: 3rem;
            width: 100%;

        }

        #topic {
            width: 80%;
             margin: 0.5rem auto;
        }

        button {
            margin: 0.1rem auto;
        }
    }

    @media only screen and (max-width: 550px) {
        button {
            padding: 0.8rem;
            margin: 0.4rem auto;
        }

        input {
            width: 100%;
            margin: 1rem auto;
            display: inline-block;
        }
    }

</style>