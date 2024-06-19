---
theme: dashboard
title: Performance du modèle
toc: false
---

# Performance du modèle

```js
// Local imports
import {lollipopFacetedChart} from "./components/lollipop.js";
import {histogramIC} from "./components/histogramIC.js";

// npm imports
import {DuckDBClient} from "npm:@observablehq/duckdb";
```

```js
const db = DuckDBClient.of({data_annotated: FileAttachment("./data/data_annotated.parquet")});
```

```js
const well_coded_rate = [...accuracies_by_level].find(d => (d.threshold == "Total") & (d.level == "Level 5"))?.accuracy
```


```js
const data = accuracies_by_level
const x = "level"
const y = "accuracy"
const fill = "accuracy"
const facet = "threshold"
const pivot = well_coded_rate
```



```js
const accuracies_by_level = db.sql`
-- Accuracy globale
SELECT
  'Total' AS threshold,
  'Level 1' AS level,
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_1 ELSE 1 END) * 100.0 AS accuracy
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Level 2',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_2 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Level 3',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_3 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Level 4',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_4 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Level 5',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 ELSE 1 END) * 100.0
FROM data_annotated

-- Performance pour les liasses en auto
UNION ALL

SELECT
  'Automatique',
  'Level 1',
  AVG(Result_level_1) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Level 2',
  AVG(Result_level_2) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Level 3',
  AVG(Result_level_3) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Level 4',
  AVG(Result_level_4) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Level 5',
  AVG(Result_level_5) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

-- Performance sur les liasses en reprise
UNION ALL

SELECT
  'Reprise',
  'Level 1',
  AVG(Result_level_1) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Level 2',
  AVG(Result_level_2) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Level 3',
  AVG(Result_level_3) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Level 4',
  AVG(Result_level_4) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Level 5',
  AVG(Result_level_5) * 100.0
FROM data_annotated
WHERE IC < ${threshold}
`
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
    <span class="big">${well_coded_rate.toFixed(2)}%</span>
  </div>
</div>



<div class="grid grid-cols-4">
  <div class="card grid-colspan-2 grid-rowspan-2">
    <h2>Change in demand by balancing authority</h2>
    <h3>Percent change in electricity demand from previous hour</h3>
    ${resize((width) => histogramIC(data_annotated, {width,
      title: "This is a title",
      IC: threshold,
      x: "IC",
      y: "Result_level_5",
      }))}
      <figcaption>
        Caption
      </figcaption>
    </figure>
  </div>
  <div class="card grid-colspan-2">
    <h2>Top 5 balancing authorities by demand on (GWh)</h2>
    ${resize((width) => lollipopFacetedChart(accuracies_by_level, {width,
      title: "This is a title",
      pivot: well_coded_rate,
      x: "level",
      y: "accuracy",
      fill: "accuracy",
      facet: "threshold",
      domain_x: ["Level 5", "Level 4", "Level 3", "Level 2", "Level 1"]
      }))}
  </div>
  <div class="card grid-colspan-2">
    <h2>US electricity generation demand vs. day-ahead forecast (GWh)</h2>
    ${resize((width) => lollipopFacetedChart(accuracies_by_k, {width,
        title: "This is a title",
        pivot: well_coded_rate,
        x: "k",
        y: "accuracy",
        fill: "accuracy",
        facet: "threshold",
        }))}
  </div>
</div>


```js
const accuracies_by_k = db.sql`
-- Performance pour les liasses en auto

SELECT
  'Automatique' AS threshold,
  'Top 1' AS k,
  AVG(Result_level_5) * 100.0 AS accuracy
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Top 2',
  AVG(Result_level_5 + Result_k_2) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Top 3',
  AVG(Result_level_5 + Result_k_2 + Result_k_3) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Top 4',
  AVG(Result_level_5 + Result_k_2 + Result_k_3 + Result_k_4) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Top 5',
  AVG(Result_level_5 + Result_k_2 + Result_k_3 + Result_k_4 + Result_k_5) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

-- Performance sur les liasses en reprise
UNION ALL

SELECT
  'Reprise',
  'Top 1',
  AVG(Result_level_5) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Top 2',
  AVG(Result_level_5 + Result_k_2) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Top 3',
  AVG(Result_level_5 + Result_k_2 + Result_k_3) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Top 4',
  AVG(Result_level_5 + Result_k_2 + Result_k_3 + Result_k_4) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Top 5',
  AVG(Result_level_5 + Result_k_2 + Result_k_3 + Result_k_4 + Result_k_5) * 100.0
FROM data_annotated
WHERE IC < ${threshold}
`
```
