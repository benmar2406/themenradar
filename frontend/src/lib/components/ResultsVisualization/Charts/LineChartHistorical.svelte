<script>
    import { scaleUtc, scaleLinear } from 'd3-scale';
    import { extent } from 'd3-array';
    import { line, curveBasis } from 'd3-shape';
    import { axisBottom, axisLeft } from 'd3-axis';
    import { draw } from 'svelte/transition';

    const colors = [
      { label: 'positiv', color: '#9DFF1C' }, 
      { label: 'neutral', color: '#FFF01C' },
      { label: 'negativ', color: '#FF7E1C' },
    ]
  
    let width = $state(500);
    const height = 300;
    const margin = { top: 10, right: 10, bottom: 30, left: 40 };
    let innerWidth = width - margin.left - margin.right;
  
    // Raw data with full ISO datetime strings
    const rawData = {
      "2024-12-01T00:00:00.000Z": { positive: 38.1, neutral: 49.2, negative: 12.7 },
      "2025-01-01T00:00:00.000Z": { positive: 34.4, neutral: 53.1, negative: 12.5 },
      "2025-02-01T00:00:00.000Z": { positive: 36.6, neutral: 52.2, negative: 11.2 },
      "2025-03-01T00:00:00.000Z": { positive: 32.8, neutral: 54.9, negative: 12.3 },
      "2025-04-01T00:00:00.000Z": { positive: 29.7, neutral: 57.8, negative: 12.5 },
      "2025-05-01T00:00:00.000Z": { positive: 41.5, neutral: 46.2, negative: 12.3 }
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
  
    let xScale, yScale, xAxisTicks = [], yAxisTicks = [];
    let linePositive, lineNeutral, lineNegative;
  
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
        .ticks(6)
        .tickFormat(d => `${d}%`)
        .scale()
        .ticks()
        .map(t => ({
          value: t,
          label: `${t}%`
        }));
  
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
  
  <div class="item-container">
    <h3>Entwicklung des Sentiments zum Thema über die Zeit</h3>
    <div class="wrapper" bind:clientWidth={width}>
      {#if width && xScale && yScale && linePositive && lineNeutral && lineNegative}
        <svg {width} {height}>
          <!-- Lines -->
          <path d={linePositive} stroke="#9DFF1C" fill="none" stroke-width="3.5" in:draw={{ duration: 1200 }} />
          <path d={lineNeutral} stroke="#FFF01C" fill="none" stroke-width="3.5" in:draw={{ duration: 1200 }} />
          <path d={lineNegative} stroke="#FF7E1C" fill="none" stroke-width="3.5" in:draw={{ duration: 1200 }} />
  
          <!-- X Axis -->
          <g transform={`translate(0, ${height - margin.bottom})`}>
            <line x1={margin.left} x2={width - margin.right} y1={0} y2={0} stroke="#999" />
            {#each xAxisTicks as tick}
              <g transform={`translate(${xScale(tick.value)}, 0)`}>
                <line y2="6" stroke="#999" />
                <text y="20" text-anchor="middle" font-size="10">{tick.label}</text>
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
    <div>
      <div class="legend-items">
        {#each colors as color}
          <div class="legend-item">
            <div class="color-legend" style="background-color: {color.color}"></div><span>{color.label}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>
  
  <style>
    .wrapper {
      width: 100%;
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
  </style>


  