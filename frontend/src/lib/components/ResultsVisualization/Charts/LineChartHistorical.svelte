<script>
  import { scaleUtc, scaleLinear } from 'd3-scale';
  import { extent } from 'd3-array';
  import { line, curveBasis } from 'd3-shape';
  import { axisBottom, axisLeft } from 'd3-axis';
  import { draw } from 'svelte/transition';
  import { innerWidth } from 'svelte/reactivity/window';


  //let { rawData } = $props();

  const colors = [
    { label: 'positiv', color: '#9DFF1C' }, 
    { label: 'neutral', color: '#FFF01C' },
    { label: 'negativ', color: '#FF7E1C' },
  ]

  let width = $state(500);
  let height = $state(300);

  $effect(() => {
    if (innerWidth.current <= 1000) {
      height = 400;
    } else {
      height = 300;
    };
  })
  
  const margin = { top: 10, right: 10, bottom: 30, left: 40 };
  
    // Raw data with full ISO datetime strings
    const rawData = {
      "2024-12-01T00:00:00.000Z": { positive: 60.1, neutral: 12.2, negative: 12.7 },
      "2025-01-01T00:00:00.000Z": { positive: 56.4, neutral: 13.1, negative: 15.5 },
      "2025-02-01T00:00:00.000Z": { positive: 50.6, neutral: 11.2, negative: 20.2 },
      "2025-03-01T00:00:00.000Z": { positive: 53.8, neutral: 13.9, negative: 25.3 },
      "2025-04-01T00:00:00.000Z": { positive: 50.7, neutral: 12.8, negative: 30.5 },
      "2025-05-01T00:00:00.000Z": { positive: 41.5, neutral: 12.2, negative: 37.3 }
    };
  
    const data_positive = Object.entries(rawData).map(([date, val]) => ({
      date: new Date(date),
      value: val.positive
    }));
  
    const data_neutral = Object.entries(rawData).map(([date, val]) => ({
      date: new Date(date),
      value: val.neutral
    }));
  
    const data_negative = Object.entries(rawData).map(([date, val]) => ({
      date: new Date(date),
      value: val.negative
    }));
  
    const germanFormatter = new Intl.DateTimeFormat('de-DE', {
      year: 'numeric',
      month: 'long'
    });
  
    let xScale = $state();
    let yScale = $state();
    let xAxisTicks = $state([]); 
    let yAxisTicks = $state([]); 
    let linePositive = $state();
    let lineNeutral = $state();
    let lineNegative = $state();
  
    $effect(() => {
      if (!width || data_positive.length === 0) return;
  
      xScale = scaleUtc()
        .domain(extent(data_positive, d => d.date))
        .range([margin.left, width - margin.right]);
  
      yScale = scaleLinear()
        .domain([0, 100])
        .range([height - margin.bottom, margin.top]);
  
      const tickCount = Math.floor(width / 80);
  
      xAxisTicks = axisBottom(xScale)
        .ticks(tickCount)
        .tickFormat(germanFormatter.format)
        .scale()
        .ticks()
        .map(t => ({
          value: t,
          label: germanFormatter.format(t)
        }));
  
      yAxisTicks = axisLeft(yScale)
        .tickFormat(d => `${d}%`)
        .scale()
        .ticks()
        .map(t => ({
          value: t,
          label: `${t}%`
        }))
        .filter((_, index) => index % 2 === 0); // Filtere, um nur jedes zweite Tick-Label zu behalten;
  
      const makeLine = (data) =>
        line()
          .x(d => xScale(d.date))
          .y(d => yScale(d.value))
          .curve(curveBasis)(data);
  
      linePositive = makeLine(data_positive);
      lineNeutral = makeLine(data_neutral);
      lineNegative = makeLine(data_negative);
    });
  </script>
  
  <figure class="item-container">
    <h3>Entwicklung des Sentiments zum Thema über die Zeit</h3>
    <div class="wrapper" bind:clientWidth={width}>
      {#if width && xScale && yScale && linePositive && lineNeutral && lineNegative}
        <svg {width} {height} class="chart">
          <!-- Lines -->
          <path d={linePositive} stroke="#9DFF1C" fill="none" stroke-width="3.5" in:draw={{ duration: 1200 }} />
          <path d={lineNeutral} stroke="#FFF01C" fill="none" stroke-width="3.5" in:draw={{ duration: 1200 }} />
          <path d={lineNegative} stroke="#FF7E1C" fill="none" stroke-width="3.5" in:draw={{ duration: 1200 }} />
  
          <!-- X Axis -->
          <g transform={`translate(0, ${height - margin.bottom})`} >
            <line x1={margin.left} x2={width - margin.right} y1={0} y2={0} stroke="#999" />
            {#each xAxisTicks as tick}
              <g transform={`translate(${xScale(tick.value)}, 0)`}>
                <line y2="6" stroke="#999" />
                <text
                  y="20"
                  text-anchor="middle"
                  font-size="10"
                  transform={innerWidth.current <= 1000 ? 'rotate(90 0 20)' : ''}
                >
                  {tick.label}
                </text>              
              </g>
            {/each}
          </g>
  
          <!-- Y Axis -->
          <g>
            <line x1={margin.left} x2={margin.left} y1={margin.top} y2={height - margin.bottom} stroke="#999" />
              {#each yAxisTicks as tick}
                <g transform={`translate(0, ${yScale(tick.value)})`}>
                  <line x1={margin.left} x2={width - margin.right} stroke="#eee" />
                  <text x={margin.left - 8} dy="0.32em" text-anchor="end" font-size="10">{tick.label}</text>
                </g>
            {/each}
          </g>
          </svg>  
      {/if}
        </div>
      <figcaption class="legend-items">
        {#each colors as color}
          <div class="legend-item">
            <div class="color-legend" style="background-color: {color.color}"></div><span>{color.label}</span>
          </div>
        {/each}
      </figcaption>
  </figure>
  
  <style>
    .wrapper {
      display: block;
      width: 90%;
      height: auto;
    }

    .chart {
      overflow: visible;
    }
  
    text {
      font-family: sans-serif;
      fill: #333;
    }

    .legend-items {
      display: flex;
      margin-top: 1.3rem;
    }
    
    .legend-item {
      display: flex;
      align-items: center;
      margin: 0.2rem 1.3rem;
    }

    .legend-item span {
      margin: 0;
      font-size: 0.8rem;
    }

    .color-legend {
      height: 1.2rem;
      width: 1.2rem;
      border-radius: 50%;
      display: inline-block;
      margin: 0.3rem;
    }

    @media only screen and (max-width: 1000px) {
    .item-container {
      margin: 3rem auto;
      width: 90%;
    }

    .chart {
      margin: auto;
    }

    .legend-items {
      justify-content: center;
    }
  }


  </style>


  