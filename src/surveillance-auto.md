---
title: Surveillance automatisation
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
const data_agg = db.query(query)
```

```js 
const aggregation = view(Inputs.select(["Section", "Division", "Groupe", "Classe", "Sous-classe"], {value: "Section", label: "Sélectionner une aggrégation"}));
```

<!-- QUERIES SQL -->

```js
const query = `
    -- Query to compute frequency 
    SELECT
        "${aggregation}",
        COUNT(*) AS Frequency
    FROM
        data_raw
    GROUP BY
        "${aggregation}"
    ORDER BY
        "${aggregation}";
`
```


```js
const data = data_agg
const title = null
const x = aggregation
const y = "Frequency"
```

```js
Plot.plot({
  title: title,
  width,
  marginLeft: 50,
  y: {
    tickFormat: "s",
    grid: true,
    label: "Nombre de liasse"
  },
  x: {
    label: null,
    tickRotate: x !== "Section" 
      ? -90
      : 0,
    ticks: x !== "Section" 
      ? [...data_agg].map((d) => d[x]).filter((_, i) => i % Math.round([...data_agg].length / 83) === 0) // getUniquePrefixValues([...data_agg].map((d) => d[x]))
      : undefined
  },
  marks: [
    Plot.ruleX(data, {
      x: x,
      y: y,
    }),
    Plot.dot(data, {
      x: x,
      y: y,
      r: 1
    }),
    Plot.ruleY([0]),
    Plot.tip(data, Plot.pointerX({
      x: x, 
      y: y, 
      format: {
        x: (d) => `${d.toLocaleString(undefined, {
          day: "numeric",
          month: "long",
          year: "numeric"
        })}`,
        stroke: (d) => `${d.toFixed(2)}%`,
        y: (d) => `${d}`,
        fx: null
      }
    }))
  ]
})
```


```js
function getUniquePrefixValues(arr) {
  const seenPrefixes = new Set();
  const result = [];

  for (let value of arr) {
    const prefix = value.slice(0, 2); // Get the first two characters as the prefix
    if (!seenPrefixes.has(prefix)) {
      seenPrefixes.add(prefix); // Add the prefix to the set
      result.push(value); // Add the value to the result array
    }
  }

  return result;
}

```