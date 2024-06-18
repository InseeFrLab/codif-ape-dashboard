import * as Plot from "npm:@observablehq/plot";

export function lollipopChart(data, {width, title, pivot=0.5, x, y, fill} = {}) {
  return Plot.plot({
  title: title,
  width,
  height: 300,
  marginLeft: 50,

  color: {
    scheme: "RdBu",
    type: "diverging",
    pivot: pivot,
    legend: true,
    percent: true,
    label: "Taux de codification (%)"
  },
  y: {
    tickFormat: "s",
    grid: true,
    label: "Nombre de liasse"
  },
  x: {
    type: "utc",
    label: "Semaine"
  },
  marks: [
    Plot.ruleX(data, {
      x: x,
      y: y,
      stroke: fill,
      strokeWidth: 1
    }),
    Plot.dot(data, {
      x: x,
      y: y,
      fill: fill,
      r: 5
    }),
    Plot.ruleY([0]),
    Plot.tip(data, Plot.pointerX({
      x: x, 
      y: y, 
      stroke: fill
    }))
  ]
});
}
