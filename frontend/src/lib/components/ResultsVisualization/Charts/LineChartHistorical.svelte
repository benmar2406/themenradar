<script>
	import { scaleUtc, scaleLinear } from 'd3-scale';
	import { extent } from 'd3-array';
	import { line, area, curveLinear } from 'd3-shape';
	import { draw } from 'svelte/transition';
	import { innerWidth } from 'svelte/reactivity/window';

	const colors = [
		{ label: 'positiv', color: '#FFD166' },
		{ label: 'neutral', color: '#FFB74D' },
		{ label: 'negativ', color: '#FF8A65' }
	];

	function createHoverPath(dPath, data, label, color) {
	return {
		d: dPath,
		fill: 'transparent',
		stroke: 'transparent',
		'stroke-width': 30,
		style: 'cursor: pointer',
		onmouseover: (e) => {
			updateTooltip(e, data, label, color);
		},
		onmousemove: (e) => {
			updateTooltip(e, data, label, color);
		},
		onmouseleave: () => {
			tooltip.visible = false;
		}
	};
}

function updateTooltip(e, data, label, color) {
	const mouseX = e.offsetX;
	const hoveredDate = xScale.invert(mouseX);

	// Find nearest data point by date
	const closest = data.reduce((a, b) =>
		Math.abs(b.date - hoveredDate) < Math.abs(a.date - hoveredDate) ? b : a
	);

	tooltip = {
		x: e.clientX,
		y: e.clientY,
		date: closest.date,
		value: closest.value,
		label,
		color,
		visible: true
	};
}


	let width = $state(500);
	let height = $state(300);

	$effect(() => {
		if (innerWidth.current <= 1000) {
			height = 500;
		} else {
			height = 300;
		}
	});

	const margin = { top: 10, right: 10, bottom: 30, left: 40 };

	const rawData = {
		'2024-12-01T00:00:00.000Z': { positive: 60.1, neutral: 12.2, negative: 12.7 },
		'2025-01-01T00:00:00.000Z': { positive: 56.4, neutral: 13.1, negative: 15.5 },
		'2025-02-01T00:00:00.000Z': { positive: 50.6, neutral: 11.2, negative: 20.2 },
		'2025-03-01T00:00:00.000Z': { positive: 53.8, neutral: 13.9, negative: 25.3 },
		'2025-04-01T00:00:00.000Z': { positive: 50.7, neutral: 12.8, negative: 30.5 },
		'2025-05-01T00:00:00.000Z': { positive: 41.5, neutral: 12.2, negative: 37.3 }
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

	let xScale = $derived(
		scaleUtc()
			.domain(extent(data_positive, (d) => d.date))
			.range([margin.left, width - margin.right])
	);

	let yScale = $derived(
		scaleLinear()
			.domain([0, 100])
			.range([height - margin.bottom, margin.top])
	);

	const makeLine = (data) =>
		line()
			.x((d) => xScale(d.date))
			.y((d) => yScale(d.value))
			.curve(curveLinear)(data);

	const makeArea = (data) =>
		area()
			.x((d) => xScale(d.date))
			.y0(height - margin.bottom)
			.y1((d) => yScale(d.value))
			.curve(curveLinear)(data);

	let linePositive = $derived(makeLine(data_positive));
	let lineNeutral = $derived(makeLine(data_neutral));
	let lineNegative = $derived(makeLine(data_negative));

	let areaPositive = $derived(makeArea(data_positive));
	let areaNeutral = $derived(makeArea(data_neutral));
	let areaNegative = $derived(makeArea(data_negative));

	// Tooltip state
	let tooltip = $state({
		x: 0,
		y: 0,
		date: null,
		value: null,
		label: '',
		color: '',
		visible: false
	});
</script>

<figure class="item-container">
	<h3>Entwicklung des Sentiments zum Thema über die Zeit</h3>
	<div class="wrapper" bind:clientWidth={width}>
		{#if width && xScale && yScale && linePositive && lineNeutral && lineNegative}
			<svg {width} {height} class="chart">
				<defs>
					<linearGradient id="gradientPositive" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#FFD166" stop-opacity="0.6" />
						<stop offset="100%" stop-color="#FFD166" stop-opacity="0" />
					</linearGradient>
					<linearGradient id="gradientNeutral" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#FFB74D" stop-opacity="0.9" />
						<stop offset="100%" stop-color="#FFB74D" stop-opacity="0.2" />
					</linearGradient>
					<linearGradient id="gradientNegative" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#FF8A65" stop-opacity="0.6" />
						<stop offset="100%" stop-color="#FF8A65" stop-opacity="0" />
					</linearGradient>
				</defs>

				<!-- Areas -->
				<path d={areaPositive} fill="url(#gradientPositive)" stroke="none" in:draw={{ duration: 1200 }} />
				<path d={areaNeutral} fill="url(#gradientNeutral)" stroke="none" in:draw={{ duration: 1200 }} />
				<path d={areaNegative} fill="url(#gradientNegative)" stroke="none" in:draw={{ duration: 1200 }} />

				<!-- Lines -->
				<path {...createHoverPath(linePositive, data_positive, 'positiv', '#FFD166')} />
				<path {...createHoverPath(areaPositive, data_positive, 'positiv', '#FFD166')} />

				<!-- Neutral -->
				<path {...createHoverPath(lineNeutral, data_neutral, 'neutral', '#FFB74D')} />
				<path {...createHoverPath(areaNeutral, data_neutral, 'neutral', '#FFB74D')} />

				<!-- Negative -->
				<path {...createHoverPath(lineNegative, data_negative, 'negativ', '#FF8A65')} />
				<path {...createHoverPath(areaNegative, data_negative, 'negativ', '#FF8A65')} />


				<!-- Axis X -->
				<g transform={`translate(0, ${height - margin.bottom})`}>
					<line x1={margin.left} x2={width - margin.right} y1={0} y2={0} stroke="#999" />
					{#each xScale.ticks(6) as tick}
						<text
							x={xScale(tick)}
							y="20"
							text-anchor="middle"
							font-size="10"
						>
							{tick.toLocaleDateString('de-DE', { month: 'short' })}
						</text>
					{/each}
				</g>

				<!-- Axis Y -->
				<g>
					<line x1={margin.left} x2={margin.left} y1={margin.top} y2={height - margin.bottom} stroke="#999" />
					{#each yScale.ticks(2) as tick}
						<g transform={`translate(0, ${yScale(tick)})`}>
							<line x1={margin.left} x2={width - margin.right} y1={0} y2={0} stroke="#eee" />
							<text x={margin.left - 10} y="4" font-size="10" text-anchor="end">{tick}%</text>
						</g>
					{/each}
				</g>
			</svg>

			{#if tooltip.visible}
				<div
					class="tooltip"
					style="
						left: {tooltip.x + 15}px;
						top: {tooltip.y + 15}px;
						border-color: {tooltip.color};
					"
				>
					<strong style="color: {tooltip.color}">{tooltip.label}</strong><br />
					{tooltip.date.toLocaleDateString('de-DE', { month: 'long', year: 'numeric' })}<br />
					Wert: {tooltip.value.toFixed(1)}%
				</div>
			{/if}
		{/if}
	</div>

	<figcaption class="legend-items">
		{#each colors as color}
			<div class="legend-item">
				<div class="color-legend" style="background-color: {color.color}"></div>
				<span>{color.label}</span>
			</div>
		{/each}
	</figcaption>
</figure>

<style>
	.wrapper {
		display: block;
		width: 95%;
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

	.tooltip {
		position: fixed;
		background: white;
		border: 1px solid;
		padding: 0.5rem 0.75rem;
		border-radius: 4px;
		font-size: 0.75rem;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		pointer-events: none;
		z-index: 10;
		white-space: nowrap;
		transition: opacity 0.2s ease;
	}

	@media only screen and (max-width: 1000px) {
		.item-container {
			margin: 3rem auto;
			width: 90%;
		}
		.wrapper {
			height: 550px;
		}
		.chart {
			margin: auto;
		}
		.legend-items {
			justify-content: center;
		}
	}
</style>
