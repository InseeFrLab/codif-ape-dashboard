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
function transformToUrl(description, top_k) {
  const baseUrl = "https://codification-ape-pytorch.lab.sspcloud.fr/predict-and-explain";
  const encodedDescription = encodeURIComponent(description);
  const fullUrl = `${baseUrl}?text_description=${encodedDescription}&prob_min=0.01&top_k=${top_k}`;

  return fullUrl;
}

function guard(fn, options = {}) {
  const {
    submitLabel = 'Submit',
    required = false,
    resubmit = true,
    width = 'fit-content',
    justify = 'start'
  } = options;

  const onSubmit = () => {
    value = input.value;
    submit.disabled = !resubmit;
    wrapper.dispatchEvent(new Event('input', { bubbles: true }));
  };
  const submit = htl.html`<button ${{disabled: !resubmit && !required, onclick: onSubmit}}>${submitLabel}`;
  const footer = htl.html`<div><hr style="padding:0;margin:10px 0"><div style="display:flex;gap:1ch;justify-content:${justify}">${submit}`;
  const template = inputs => htl.html`<div>${
    Array.isArray(inputs) ? inputs : Object.values(inputs)
  }${footer}`;
  
  const input = fn({submit, footer, template, onSubmit});
  input.addEventListener('input', (e) => {
    e.stopPropagation();
    submit.disabled = false;
  });
  let value = required ? undefined : input.value;
  const wrapper = htl.html`<div style="width:${width}">${input}`;
  wrapper.addEventListener('submit', onSubmit);
  return Object.defineProperty(wrapper, 'value', {
    get: () => value,
    set: (v) => { input.value = v },
  });
}
```

```js
const inputs = view( guard(
  // The callback. We pass `template` through to Inputs.form(), but could also
  // define our own template instead. See "Callback context" in the documentation.
  ({ template }) => Inputs.form(
    {
      text: Inputs.textarea({label: "Description APE", rows:2, cols:100, placeholder: "Entrez votre description", value: "Institut National de la Statistique et de l'Administration Economique"}),
      topk: Inputs.range([0, 10], {value: 5, step: 1, label: "Nombre de prédictions (par ordre décroissant de confiance)"})
    },
    { template }
  )
)
)
```

```js
const top_k = inputs["topk"]
```

```js
const activite = inputs["text"]
```


```js
const urlApe = transformToUrl(activite, top_k)
```

```js
const predictions = d3.json(urlApe)
```
```js
const predictions_arr = Object.values(predictions)
```

```js
Inputs.table(
  predictions_arr, {
    format: {
     probabilite: (d) => d.toFixed(3)},

     columns: [
    "code",
    "libelle",
    "probabilite",
  ],
  header: {
    code: "Code NAF",
    libelle: "Libellé",
    probabilite:"Score de confiance"
  }
    }
)
```
```js
const letters = activite.split('').filter(letter => letter != ' ')
```

```js
const  chosen_label = view(
  Inputs.select(predictions_arr, {label: "Expliquer la prédiction:", format: x=>x.code, value:predictions_arr[0].code})
)
```

```js
const words = activite.split(" ").filter(word => word !== "");
```

```js
const aggregateWords = view(Inputs.toggle({
  label: "Aggréger au niveau mots"
}))
```

```js
const lettersData = letters.map((letter, i) => ({
        x: `${letter}_${i}`, 
        y: chosen_label.letter_attr[i], 
        code: chosen_label.code,
        letter: letter,
        idx: i,
      }))
```

```js
const lettersDomain = letters.map((letter, i) => `${letter}_${i}`)
```

```js
const wordsDomain = words.map((word, i) => `${word}_${i}`)
```

```js
const wordsData = words.map((word, i) => ({
        x: `${word}_${i}`, 
        y: chosen_label.word_attr[i], 
        code: chosen_label.code,
        word:word,
        idx:i,
      }))
```

```js
const data_to_plot = (aggregateWords == true) ? wordsData : lettersData
```
```js
const domain_to_plot = (aggregateWords == true) ? wordsDomain : lettersDomain
```
```js
Plot.plot({
  marks: [
    Plot.barY(
      data_to_plot,
      { 
        x: "x", 
        y: "y", 
        fill: "code",
      }
    )
  ],
  x: { label: "", tickFormat: d => d.split('_')[0], domain:domain_to_plot },
  y: { label: "Score d'influence", grid: true },
  color: { scheme: "Tableau10", legend: true },
})
```