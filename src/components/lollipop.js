import * as Plot from "npm:@observablehq/plot";

export function lollipopChart(data, {width, title, pivot=0.5, x, y, fill, label_x} = {}) {
  return Plot.plot({
  title: title,
  width,
  marginLeft: 50,

  color: {
    scheme: "RdBu",
    type: "diverging-pow",
    pivot: pivot,
    symmetric: false,
    legend: true,
    percent: true,
    label: "Taux de codification"
  },
  y: {
    tickFormat: "s",
    grid: true,
    label: "Nombre de liasse"
  },
  x: {
    type: "utc",
    label: label_x
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
      stroke: fill,
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
});
}



export function lollipopFacetedChart(data, {width, title, pivot=0.5, x, y, fill, facet, domain_x} = {}) {
  return Plot.plot({
  title: title,
  width,
  height: width * 0.35,
  marginLeft: 50,

  color: {
    scheme: "RdBu",
    type: "diverging-pow",
    pivot: pivot,
    symmetric: false,
    legend: true,
    percent: false,
    label: "Performance",
    // domain: [0, 100]
  },
  facet: {
    data: data, 
    x: facet,
    label: null,
    domain: ["Total", "Reprise", "Automatique"]},
  y: {
    grid: true,
    label: "Performance",
    domain: [0, 100]
  },
  x: {
    grid: false,
    label: "Aggrégation",
    domain: domain_x,
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
      stroke: fill,
      x: x,
      y: y,
      format: {
        stroke: (d) => `${d.toFixed(2)}%`,
        y: null,
        fx: null
      }
    }))
  ]
})
}
