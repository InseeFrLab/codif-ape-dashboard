---
theme: dashboard
title: Performance du modèle
toc: false
---


```js
// Local imports
import {lollipopChart} from "./components/lollipop.js";

// npm imports
import {DuckDBClient} from "npm:@observablehq/duckdb";
```
```js
```

```js
const db = DuckDBClient.of({data_annotated: FileAttachment("./data/data_annotated.parquet")});
```



```js
const data_annotated = db.sql`
                        SELECT * 
                        FROM data_annotated
                        `

const stats_desc = db.queryRow(`
                          SELECT 
                            COUNT(*) AS nb_liasse, 
                            COUNT(CASE WHEN data_annotated."Response.IC" > ${threshold} THEN 1 END ) * 100.0 / COUNT(*) AS auto_rate,
                          FROM data_annotated
                          `)

const weekly_stats = db.sql`
                    SELECT
                      DATE_TRUNC('week', date) AS week_start,
                      COUNT(CASE WHEN data_annotated."Response.IC" > ${threshold} THEN 1 END) / COUNT(*) AS auto_rate,
                      COUNT(*) AS nb_liasse, 
                    FROM data_annotated
                    GROUP BY DATE_TRUNC('week', date);
                    `

const daily_stats = db.sql`
                    SELECT
                      date,
                      COUNT(CASE WHEN data_annotated."Response.IC" > ${threshold} THEN 1 END) / COUNT(*) AS auto_rate,
                      COUNT(*) AS nb_liasse, 
                    FROM data_annotated
                    GROUP BY date;
                    `
```

```js
const thresholdInput = Inputs.range([0, 1], {step: .01, value: 0.8});
const threshold = Generators.input(thresholdInput);
```

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

```js
Inputs.table(data_annotated)
```