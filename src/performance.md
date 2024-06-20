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

// Data imports
const db = DuckDBClient.of({data_annotated: FileAttachment("./data/data_annotated.parquet")});
```

```js
const well_coded_rate = [...accuracies_by_level].find(d => (d.threshold == "Total") & (d.level == "Sous-classe"))?.accuracy
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
const data_histo = db.sql`
                        SELECT IC, Result_level_5 
                        FROM data_annotated
                        `

const stats_desc = db.queryRow(`
                          SELECT 
                            COUNT(*) AS nb_liasse, 
                            COUNT(CASE WHEN data_annotated.IC >= ${threshold} THEN 1 END ) * 100.0 / COUNT(*) AS auto_rate,
                          FROM data_annotated
                          `)
```

```js
const thresholdInput = Inputs.range([0, 1], {step: .01, value: 0.8});
const threshold = Generators.input(thresholdInput);
```

```js
function centerResize(render) {
  const div = resize(render);
  div.style.display = "flex";
  div.style.flexDirection = "column";
  div.style.alignItems = "center";
  return div;
}
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
    <h2>Distribution des indices de confiances en fonction du résultat de la codification</h2>
    <h3></h3>
      <figure style="max-width: none;">
      ${centerResize((width) => histogramIC(data_histo, {width,
        IC: threshold,
        x: "IC",
        y: "Result_level_5",
        }))}
      </figure>
  </div>
  <div class="card grid-colspan-2">
    <h2>Performance du modèle pour les différents niveaux de la nomenclature</h2>
    ${resize((width) => lollipopFacetedChart(accuracies_by_level, {width,
      pivot: well_coded_rate,
      x: "level",
      y: "accuracy",
      fill: "accuracy",
      facet: "threshold",
      domain_x: ["Sous-classe", "Classe", "Groupe", "Division", "Section"]
      }))}
  </div>
  <div class="card grid-colspan-2">
    <h2>Performance du modèle pour les 5 premiers échos renvoyés</h2>
    ${resize((width) => lollipopFacetedChart(accuracies_by_k, {width,
        pivot: well_coded_rate,
        x: "k",
        y: "accuracy",
        fill: "accuracy",
        facet: "threshold",
        }))}
  </div>
</div>


<!-- SQL QUERIES -->

```js
const accuracies_by_level = db.sql`
-- Accuracy globale
SELECT
  'Total' AS threshold,
  'Section' AS level,
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_1 ELSE 1 END) * 100.0 AS accuracy
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Division',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_2 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Groupe',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_3 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Classe',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_4 ELSE 1 END) * 100.0
FROM data_annotated

UNION ALL

SELECT
  'Total',
  'Sous-classe',
  AVG(CASE WHEN data_annotated.IC > ${threshold} THEN Result_level_5 ELSE 1 END) * 100.0
FROM data_annotated

-- Performance pour les liasses en auto
UNION ALL

SELECT
  'Automatique',
  'Section',
  AVG(Result_level_1) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Division',
  AVG(Result_level_2) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Groupe',
  AVG(Result_level_3) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Classe',
  AVG(Result_level_4) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

UNION ALL

SELECT
  'Automatique',
  'Sous-classe',
  AVG(Result_level_5) * 100.0
FROM data_annotated
WHERE IC >= ${threshold}

-- Performance sur les liasses en reprise
UNION ALL

SELECT
  'Reprise',
  'Section',
  AVG(Result_level_1) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Division',
  AVG(Result_level_2) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Groupe',
  AVG(Result_level_3) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Classe',
  AVG(Result_level_4) * 100.0
FROM data_annotated
WHERE IC < ${threshold}

UNION ALL

SELECT
  'Reprise',
  'Sous-classe',
  AVG(Result_level_5) * 100.0
FROM data_annotated
WHERE IC < ${threshold}
`
```


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
