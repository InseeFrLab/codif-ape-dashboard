---
theme: dashboard
toc: false
---

```js
// Local imports
import {lollipopChart} from "./components/lollipop.js";

// npm imports
import {DuckDBClient} from "npm:@observablehq/duckdb";

// Data imports
const db = DuckDBClient.of({data_raw: FileAttachment("./data/data_raw.parquet")});
```

```js
const thresholdInput = Inputs.range([0, 1], {step: .01, value: 0.8});
const threshold = Generators.input(thresholdInput);
```

<div class="hero">
  <h1>Tableau de bord de surveillance</h1>
  <h2> Pour la codification automatique pour la nomenclature APE</h2>
</div>


<div class="grid grid-cols-3">
  <div class="card">
    <h2>Seuil d'indice de confiance utilisé</h2>
    <span class="big">${thresholdInput}</span>
  </div>
  <div class="card">
    <h2>Nombre de liasses</h2>
    <span class="big">${stats_desc.nb_liasse}</span>
  </div>
  <div class="card">
    <h2>Pourcentage de codification automatique</h2>
    <span class="big">${stats_desc.auto_rate.toFixed(2)}%</span>
  </div>
</div>


<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => lollipopChart(weekly_stats, {width,
     pivot: stats_desc.auto_rate,
     x: "week_start",
     y: "nb_liasse",
     fill: "auto_rate",
     label_x: "Semaine"
     }))}
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => lollipopChart(daily_stats, {width,
     pivot: stats_desc.auto_rate,
     x: "date",
     y: "nb_liasse",
     fill: "auto_rate",
     label_x: "Jour"
     }))}
  </div>
</div>


<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>

<!-- QUERIES SQL -->

```js
const data_raw = db.sql`
                        SELECT * 
                        FROM data_raw
                        `

const stats_desc = db.queryRow(`
                          SELECT 
                            COUNT(*) AS nb_liasse, 
                            COUNT(CASE WHEN data_raw."Response.IC" >= ${threshold} THEN 1 END ) * 100.0 / COUNT(*) AS auto_rate,
                          FROM data_raw
                          `)

const weekly_stats = db.sql`
                    SELECT
                      DATE_TRUNC('week', date) AS week_start,
                      COUNT(CASE WHEN data_raw."Response.IC" >= ${threshold} THEN 1 END) / COUNT(*) AS auto_rate,
                      COUNT(*) AS nb_liasse, 
                    FROM data_raw
                    GROUP BY DATE_TRUNC('week', date);
                    `

const daily_stats = db.sql`
                    SELECT
                      date,
                      COUNT(CASE WHEN data_raw."Response.IC" >= ${threshold} THEN 1 END) / COUNT(*) AS auto_rate,
                      COUNT(*) AS nb_liasse, 
                    FROM data_raw
                    GROUP BY date;
                    `
```