import * as Plot from "npm:@observablehq/plot";

export function bootstrapPlot(data, {width, title, pivot, x, y, y1, y2} = {}) {
  return Plot.plot({
    title: title,
    width,
    height: width * 0.35,
    marginLeft: 50,
    color: {
      scheme: "RdBu",
      type: "diverging-pow",
      pivot: pivot,
      symmetric: true,
      legend: true,
      percent: true,
      label: "Performance",
      // domain: [0, 100]
    },
    x: {type: "utc", grid: false, label: "Mois"},
    y: {grid: true, domain: [0,100], percent: true, label: "Performance"},
    marks: [
      Plot.areaY(data, {x: x, y1: y1, y2: y2, sort: x, fillOpacity: 0.3}),
      Plot.line(data, {x: x, y: y, z: null, sort: x, stroke: y}),
      Plot.ruleY([0]),
      Plot.tip(data, Plot.pointer({
        x: x,
        y: y,
        channels: {"Borne inf": y1, "Borne sup": y2},
        format: {
          x: (d) => `${d.toLocaleString(undefined, {
            month: "long",
            year: "numeric"
          })}`,
          y: (d) => `${d.toFixed(2)}%`,
          "Borne inf": (d) => `${(d*100).toFixed(2)}%`,
          "Borne sup": (d) => `${(d*100).toFixed(2)}%`,
        }
      }))
    ]
  })
}
