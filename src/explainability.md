---
title: Explicabilité
theme: dashboard
toc: false
---

## Explicabilité
```js
import * as Plot from "npm:@observablehq/plot";
```
Entrez la description d'une Activité Principale d'Entreprise (APE) puis cliquez sur Submit.
Le graphe représente l'influence de chaque terme sur la prediction finale.


```js
function transformToUrl(description) {
  const baseUrl = "https://codification-ape-pytorch.lab.sspcloud.fr/predict-and-explain";
  const encodedDescription = encodeURIComponent(description);
  const fullUrl = `${baseUrl}?text_description=${encodedDescription}&prob_min=0.01`;
  return fullUrl;
}
```

```js
const activite = view(
  Inputs.textarea({label: "Description APE", rows:2, cols:100, placeholder: "Entrez votre description", value: "Institut National de la Statistique et de l'Administration Economique", submit: true})
)
```

```js
const urlApe = transformToUrl(activite)
```

```js
const toto = d3.json(urlApe)
```
```js
const obj = toto[1]
```

<table>
  <tr>
    <th style="text-align:center;">Libellé (NA2008)</th>
    <th>Probabilité</th>
  </tr>
    <tr>
      <td>${obj.code} | ${obj.libelle}</td>
      <td>${obj.probabilite.toFixed(3)}</td>
    </tr>
</table>

```js
const values = toto[activite]
```

```js
const words = activite.split(" ").filter(word => word !== "");
```

```js
Plot.plot({
  marks: [
    Plot.barY(words.map((word, i) => ({ word: `${word}_${i}`, value: values[i] })), {
      x: "word",  // Unique identifier for the x-axis
      y: "value",
      fill: "steelblue"
    })
  ],
  x: {
    label: "",
    tickFormat: (d) => d.split('_')[0],  // Show only the word, not the index
    domain: words.map((word, i) => `${word}_${i}`)  // Maintain the original order
  },
  y: { label: "Score d'influence", grid: true }
})
```
