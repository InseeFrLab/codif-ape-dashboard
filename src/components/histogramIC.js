import * as Plot from "npm:@observablehq/plot";

export function histogramIC(data, {width, title, IC, thresholds=50, x, y} = {}) {
  return Plot.plot({
    title: title,
    width,
    height: width * 0.8,
    marginLeft: 50,
    y: {grid: true, label: "Fréquence"},
    x: {grid: false, label: "Indice de confiance"},
    color: {
      label: ["Résultat :"], 
      legend: true,
      domain: ["Mauvaise prédiction", "Bonne prédiction"],
      range: ["#b2182b","#2166ac"],
      },
    marks: [
      Plot.rectY(data, 
        Plot.binX(
          {y: "sum"}, 
          {x: {thresholds: thresholds, value: x, domain: [0, 1]},
           y: (d) => d[y] === 1 ? 1 : -1, 
           fill: (d) => d[y] === 1 ? "Bonne prédiction" : "Mauvaise prédiction" , 
           insetLeft: 2,
           tip: {
            format: {
              y: (d) => `${d < 0 ? d * -1 : d}`,
              x: (d) => `${d}`,
              fill: (d) => `${d ? "Bonne prédiction" : "Mauvaise prédiction"}`,
            }
            },
        })),
      Plot.ruleX([IC], {stroke: "white"}),
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
}
