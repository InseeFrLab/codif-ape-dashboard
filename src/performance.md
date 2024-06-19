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
                            COUNT(CASE WHEN data_annotated.IC >= ${threshold} THEN 1 END ) * 100.0 / COUNT(*) AS auto_rate,
                          FROM data_annotated
                          `)

const accuracies_by_level = db.queryRow(`
                    SELECT
                      AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_1 ELSE 1 END) * 100.0 AS accuracy_level_1,
                      AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_2 ELSE 1 END) * 100.0 AS accuracy_level_2,
                      AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_3 ELSE 1 END) * 100.0 AS accuracy_level_3,
                      AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_4 ELSE 1 END) * 100.0 AS accuracy_level_4,
                      AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 ELSE 1 END) * 100.0 AS accuracy_level_5,
                    FROM data_annotated;
                    `)

const daily_stats = db.sql`
                    SELECT
                      date,
                      COUNT(CASE WHEN data_annotated.IC >= ${threshold} THEN 1 END) / COUNT(*) AS auto_rate,
                      COUNT(*) AS nb_liasse, 
                    FROM data_annotated
                    GROUP BY date;
                    `
```

```js
const thresholdInput = Inputs.range([0, 1], {step: .01, value: 0.8});
const threshold = Generators.input(thresholdInput);
```

<div class="grid grid-cols-4">
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
  <div class="card">
    <h2>Taux de bon codage</h2>
    <span class="big">${accuracies_by_level.accuracy_level_5.toFixed(2)}%</span>
  </div>
</div>

```js
Inputs.table(data_annotated)
```


```js
Plot.plot({
  y: {grid: true},
  color: { legend: true },
  marks: [
    Plot.rectY(data_annotated, Plot.binX({y: "sum"}, {x: {thresholds: 50, value: "IC"}, y: (d) => d.Result_level_1 === true ? 1 : -1, fill: "Result_level_1", tip: true, insetLeft: 2}))

    ]
})
```


```js
Plot.plot({
  y: {grid: true},
  x: {percent: true},
  color: { legend: true },
  marks: [
    Plot.rectY(data_annotated, Plot.binX({y2: "count"}, 
      {x: {thresholds: 50, value: "IC", label: "Indice de confiance"}, 
      fill: "Result_level_1", 
      mixBlendMode: "screen",
      channels: {
        name: "name",
        x: {
          value: "IC",
          label: "Indice de confiance"
        },
        sport: "sport"
      },
      tip: {
        format: {
          name: true,
          sport: true,
          nationality: true,
          y: (d) => `${d}m`,
          x: (d) => `${d}`,
          stroke: false
        }
      }
      })),
    Plot.ruleY([0]),
  ]
})
```