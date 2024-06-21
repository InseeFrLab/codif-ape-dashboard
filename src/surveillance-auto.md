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

<!-- QUERIES SQL -->

```js
const data_raw = db.sql`
        CREATE TABLE naf_sections_mapping (
            code VARCHAR(10),
            Section CHAR(1)
        );

        -- Insert mappings into the table
        INSERT INTO naf_sections_mapping (code, Section) VALUES
        ('01', 'A'), ('02', 'A'), ('03', 'A'), ('05', 'B'), ('06', 'B'), ('07', 'B'), ('08', 'B'), ('09', 'B'), ('10', 'C'), ('11', 'C'), ('12', 'C'), ('13', 'C'), ('14', 'C'), ('15', 'C'), ('16', 'C'), ('17', 'C'), ('18', 'C'), ('19', 'C'), ('20', 'C'), ('21', 'C'), ('22', 'C'), ('23', 'C'), ('24', 'C'), ('25', 'C'), ('26', 'C'), ('27', 'C'), ('28', 'C'), ('29', 'C'), ('30', 'C'), ('31', 'C'), ('32', 'C'), ('33', 'C'), ('35', 'D'), ('36', 'E'), ('37', 'E'), ('38', 'E'), ('39', 'E'), ('41', 'F'), ('42', 'F'), ('43', 'F'), ('45', 'G'), ('46', 'G'), ('47', 'G'), ('49', 'H'), ('50', 'H'), ('51', 'H'), ('52', 'H'), ('53', 'H'), ('55', 'I'), ('56', 'I'), ('58', 'J'), ('59', 'J'), ('60', 'J'), ('61', 'J'), ('62', 'J'), ('63', 'J'), ('64', 'K'), ('65', 'K'), ('66', 'K'), ('68', 'L'), ('69', 'M'), ('70', 'M'), ('71', 'M'), ('72', 'M'), ('73', 'M'), ('74', 'M'), ('75', 'M'), ('77', 'N'), ('78', 'N'), ('79', 'N'), ('80', 'N'), ('81', 'N'), ('82', 'N'), ('84', 'O'), ('85', 'P'), ('86', 'Q'), ('87', 'Q'), ('88', 'Q'), ('90', 'R'), ('91', 'R'), ('92', 'R'), ('93', 'R'), ('94', 'S'), ('95', 'S'), ('96', 'S'), ('97', 'T'), ('98', 'T'), ('99', 'U');

        WITH initial_result AS (
            SELECT
                d."Response.1.code" AS "Sous-classe",
                SUBSTRING(d."Response.1.code", 1, 4) AS Classe,
                SUBSTRING(d."Response.1.code", 1, 3) AS Groupe,
                response1.Section AS Section,
                response1.code AS Division
            FROM
                data_raw d
            LEFT JOIN
                naf_sections_mapping response1 ON SUBSTRING(d."Response.1.code", 1, 2) = response1.code
        )

        -- Query to compute frequency 
        SELECT
            Division,
            COUNT(*) AS Frequency
        FROM
            initial_result
        GROUP BY
            Division
        ORDER BY
            Division;
`
```

```js 
const ddd = "Division"

```

```js
Inputs.table(data_raw)
```


```js
const data = data_raw
const title = null
const x = "Division"
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
    label: null
  },
  marks: [
    Plot.ruleX(data, {
      x: x,
      y: y,
    }),
    Plot.dot(data, {
      x: x,
      y: y,
      r: 5
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
