---
title: Explicabilité
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
