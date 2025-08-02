

<section class="informational">
    <article class="informational-article">
        <h3>Willkommen beim Themenradar</h3>
        <p>Mit dem Themenradar analysierst du schnell und einfach, wie über bestimmte Themen in Texten gesprochen wird.</p>
        <p>Gib ein Thema und einen Text ein – das KI-gestützte System bewertet, ob der Text positiv, neutral oder negativ über dein Thema berichtet und wie sich die Stimmung zu dem Thema über die Zeit verändert hat.</p>
        <p>So erhältst du in Sekundenschnelle einen Eindruck davon, wie die öffentliche Wahrnehmung deiner Themen gestaltet ist.</p>
    </article>
    <div class="informational-image">
        <img src="/images/magazines.webp" alt="radar chart"/>
    </div>
</section>

<style>
    .informational {
        display: flex;
        margin: auto;
        width: 100%;
        text-align: center;
        background-color: var(--primary);
        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px; 
    }

    .informational-article {    
        flex-basis: 40%;
        margin: 2.5rem;
        margin-left: 8rem;
    }

    .informational-image {
        flex-basis: 50%;
        height: 450px;
        overflow: hidden;
    }

    .informational-image img {
        object-fit: cover;
        width: 100%;
        height: 100%;
    }

    @media only screen and (max-width: 900px) {
        .informational {
           display: block;
        }

        .informational-article {    
            margin: 3rem;
        }

        .informational-image {
            display: none;
        }
    }

    @media only screen and (max-width: 670px) {
        .informational-article {
            margin: 1rem auto;
        }

        .informational {
            margin: 2rem auto;
        }
    }

</style>
