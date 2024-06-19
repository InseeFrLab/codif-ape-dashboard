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
const well_coded_rate = [...accuracies_by_level].find(d => (d.threshold == "All") & (d.level == "Level 5"))?.accuracy
```

```js
Inputs.table(data_annotated)
```

```js
Inputs.table(accuracies_by_k)
```

```js
const accuracies_by_level = db.sql`
-- Accuracy globale
SELECT
  'All' AS threshold,
  'Level 1' AS level,
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_1 ELSE 1 END) * 100.0 AS accuracy
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Level 2',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_2 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Level 3',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_3 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Level 4',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_4 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'All',
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


```js
Plot.plot({
  y: {grid: true, label: "Fréquence :"},
  x: {grid: false, label: "Indice de confiance :"},
  color: {label: ["Résultat :"], legend: true},
  marks: [
    Plot.rectY(data_annotated, 
      Plot.binX(
        {y: "sum"}, 
        {x: {thresholds: 50, value: "IC", domain: [0, 1]},
         y: (d) => d.Result_level_1 === 1 ? 1 : -1, 
         fill: (d) => d.Result_level_1 === 1 ? "Bonne prédiction" : "Mauvaise prédiction" , 
         insetLeft: 2,
         tip: {
          format: {
            y: (d) => `${d < 0 ? d * -1 : d}`,
            x: (d) => `${d}`,
            fill: (d) => `${d ? "Bonne prédiction" : "Mauvaise prédiction"}`,
          }
          },
      })),
    Plot.ruleX([threshold], {stroke: "red"}),
    // Plot.text(
    //   [` ← Liasses envoyée en reprise gestionnaire`],
    //   {x: threshold - 0.18 , y: 2600, anchor: "middle"}
    // ),
    // Plot.text(
    //   [`Liasses codées automatiquement →`],
    //   {x: threshold + 0.15, y: 2600, anchor: "middle"}
    // ),
    ]
})
```



```js
const accuracies_by_k = db.sql`
-- Accuracy globale
SELECT
  'All' AS threshold,
  'Top 1' AS k,
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 ELSE 1 END) * 100.0 AS accuracy
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Top 2',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 + Result_k_2 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Top 3',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 + Result_k_2 + Result_k_3 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Top 4',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 + Result_k_2 + Result_k_3 + Result_k_4 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'All',
  'Top 5',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 + Result_k_2 + Result_k_3 + Result_k_4 + Result_k_5 ELSE 1 END) * 100.0
FROM data_annotated

-- Performance pour les liasses en auto
UNION ALL

SELECT
  'Automatique',
  'Top 1',
  AVG(Result_level_5) * 100.0
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
