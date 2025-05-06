<script>
  import { arc, pie } from "d3-shape";
  import { scaleOrdinal } from "d3-scale";
  import { interpolate } from "d3-interpolate";
  import { select } from "d3-selection";
  import { fade } from "svelte/transition";

  // Svelte 5: access reactive props
  let { data, topic, resolvedTopic } = $props();

  let pieData = $state()


  let height = 360;
  let width = height;

  // Color scale by tone
  const colorScale = scaleOrdinal()
    .domain(["positive", "neutral", "negative"])
    .range(["#fff01c", "#FFF9B0", "#FFCC33"]);

  // Arc generators
  const arcGenerator = arc()
    .innerRadius((0.5 * height) / 2.4)
    .outerRadius((0.8 * height) / 2.2)
    .cornerRadius(4);

  const labelArcs = arc()
    .innerRadius((0.9 * height) / 2.1)
    .outerRadius((0.87 * height) / 2);

  // Compute pie layout
  const pieGenerator = pie()
    .value(d => d.percentage)
    .sort(null);

  $effect(() => {
    if (!data || data.length === 0) {
      pieData= [];
    } else {
    pieData = pieGenerator(data)
    }
  })  


  // Animation transition for each slice
  const reveal = (node, { index }) => {
    const d = pieData[index];
    const start = +d.startAngle;
    const end = +d.endAngle;
    let i = interpolate(start, end);
    return {
      delay: index * (end - start) * 20 + 300,
      duration: 400,
      tick: (t) => {
        d.endAngle = i(t);
        select(node).attr("d", arcGenerator(d));
      }
    };
  };
</script>
<div class="pie-chart-container">
<h3 class="pie-chart-title">Verteilung der Stimmung</h3>
<svg {width} {height} viewBox="0 0 {width} {height}" class="chart">
  <g transform="translate({width / 2} {height / 2.3 })">
    {#each pieData as d, i (d.data.tone)}
      <path
        in:reveal={{ index: i }}
        d={arcGenerator(d)}
        fill={colorScale(d.data.tone)}
        stroke="white"
        stroke-width="2"
      />
      {#if d.data.percentage > 0}
        <text
          in:fade={{ delay: 800 }}
          font-size="0.75em"
          text-anchor="middle"
          class="fill-black-100"
          transform="translate({labelArcs.centroid(d).join(',')})"
        >
          {d.data.tone}
        </text>
        <text
          in:fade={{ delay: 1000 }}
          font-size="0.75em"
          font-weight="bold"
          text-anchor="middle"
          transform="translate({labelArcs.centroid(d).join(',')})"
          y="1.2em"
          class="fill-black-100"
        >
          {d.data.percentage}%
        </text>
        {/if}
    {/each}
  </g>
</svg>
</div>

<style>

  .pie-chart-container {
    width: fit-content;
    margin: 2rem;
  }

  .chart {
    max-width: 100%;
    height: fit-content;
    display: block;
    overflow: "visible";
  }

  .pie-chart-title {
    text-align: center;
  }

  .fill-black-100 {
    fill: #1E1E1E;
  }
</style>
