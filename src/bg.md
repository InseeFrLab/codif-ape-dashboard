# coucou


```js
import {DuckDBClient} from "npm:@observablehq/duckdb";
```

```js
const db = DuckDBClient.of({data_raw: FileAttachment("./data/data_raw.parquet")});
```

```js
const data_raw = db.sql`SELECT * 
                        FROM data_raw`

const stats_desc = db.queryRow(`SELECT 
                            COUNT(*) AS nb_liasse, 
                            (COUNT( 
                                CASE WHEN data_raw."Response.IC" > ${threshold} THEN 1 END 
                                ) * 100.0 / COUNT(*) 
                            ) AS auto_rate 
                          FROM data_raw`)

const weekly_auto_rates = db.sql`SELECT
                      DATE_TRUNC('week', date) AS week_start,
                      (COUNT(
                          CASE WHEN data_raw."Response.IC" > ${threshold} THEN 1 END
                          ) / COUNT(*)
                      ) AS auto_rate
                    FROM data_raw
                    GROUP BY DATE_TRUNC('week', date);`

const daily_auto_rates = db.sql`SELECT
                      date,
                      (COUNT(
                          CASE WHEN data_raw."Response.IC" > ${threshold} THEN 1 END
                          ) / COUNT(*)
                      ) AS auto_rate
                    FROM data_raw
                    GROUP BY date;`
```

```js
const threshold = view(Inputs.range([0, 1], {step: .01, value: 0.8}));
```

```js
Inputs.table(data_raw, {
  format: {
    date: (x) => new Date(x).toISOString().slice(0, 10),
    Timestamp: (x) => new Date(x).toISOString().slice(0, 10)
  }
})
```

```js
display(stats_desc)
```


```js

```

```js
Inputs.table(weekly_auto_rates, {
  format: {
    week_start: (x) => new Date(x).toISOString().slice(0, 10),
  }
})
```

```js
Inputs.table(daily_auto_rates, {
  format: {
    date: (x) => new Date(x).toISOString().slice(0, 10),
  }
})
```