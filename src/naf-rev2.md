---
title: Codification en NAF rev 2
theme: dashboard
toc: false
---

# Codification en NAF rev 2

Entrez la description d'une Activité Principale d'Entreprise (APE)


<div class="grid grid-cols-4">
  <div class="card grid-colspan-3">
    <h2>Description de l'activité principale de l'entreprise</h2>
    <span class="big">${activityInput}</span>
  </div>
  <div class="card grid-colspan-1">
    <h2>Catégorie juridique</h2>
    <span class="big">${cjInput}</span>
  </div>
</div>


<div class="grid grid-cols-3">
  <div class="card">
    <h2>Type de la liasse</h2>
    <span class="big">${typeFormInput}</span>
  </div>
  <div class="card">
    <h2>Surface</h2>
    <span class="big">${surfInputDisplay}</span>
  </div>
  <div class="card">
    <h2>Caractère permanent ou saisonnier</h2>
    <span class="big">${permStatusInput}</span>
  </div>
</div>


<div class="grid grid-cols-3">
  <div class="card">
    <h2>Nature de l'activité</h2>
    <span class="big">${natInputDisplay}</span>
  </div>
  <div class="card">
    <h2>Autre nature d'activité</h2>
    <span class="big">${otherNatureActivityInput}</span>
  </div>
  <div class="card">
    <h2>Précision sur les activités secondaires agricoles</h2>
    <span class="big">${precActivSecAgriInput}</span>
  </div>
</div>

# Résultats de la prédiction 
 
<div class="grid grid-cols-3 grid-rowspan-2">
  <div class="card grid-colspan-1 grid-rowspan-2">
    <h1 class="results">${predictions_arr[0].code} 🥇</h1>
    <h2>${predictions_arr[0].libelle}</h2>
    <h3>Confiance : ${(predictions_arr[0].probabilite * 100).toFixed(2)}%</h3>
  </div>

  <div class="card grid-colspan-1 grid-rowspan-2">
    <h1 class="results">${predictions_arr[1].code} 🥈</h1>
    <h2>${predictions_arr[1].libelle}</h2>
    <h3>Confiance : ${(predictions_arr[1].probabilite * 100).toFixed(2)}%</h3>
  </div>

  <div class="card grid-colspan-1 grid-rowspan-2">
    <h1 class="results">${predictions_arr[2].code} 🥉</h1>
    <h2>${predictions_arr[2].libelle}</h2>
    <h3>Confiance : ${(predictions_arr[2].probabilite * 100).toFixed(2)}%</h3>
  </div>
</div>


  <div class="card">
    <h1>Indice de confiance :</h1>
    <canvas id="canvas" width="1200" height="30" style="max-width: 100%; height: 30px;"></canvas>
    <h2>Score: ${((predictions_arr[0].probabilite - predictions_arr[1].probabilite) * 100).toFixed(2)}%</h2>
    <h3>Type de codification:${(predictions_arr[0].probabilite - predictions_arr[1].probabilite) < 0.7 ? "en reprise gestionnaire" : "automatique" }</h3>
  </div>



```js
const activityInput = Inputs.text({width: width*0.9, placeholder: "Entrez votre description"})
const activity = Generators.input(activityInput);

const CJRegex =/^\d{4}/ ;
const cjInput = Inputs.text({
  placeholder: "Entrez un code à 4 chiffres",
  // validate: (value) => CJRegex.test(value),
  error: "Doit être code à 4 chiffres"
});
const cj = Generators.input(cjInput);


const typeFormInput = Inputs.select(["A","B","C","D","E","G","I","L","M","N","P","R","S","X","Y","Z",])
const typeForm = Generators.input(typeFormInput);

const surfOptionsDisplay = [
  "1 - strictement inférieure à 120 m2",
  "2 - entre 120 et 399 m2",
  "3 - entre 400 et 2499 m2",
  "4 - strictement supérieure à 2499 m2"
];
const surfOptions = surfOptionsDisplay.map(option => option.split(" - ")[0]);
const surfInputDisplay = Inputs.select([null].concat(surfOptionsDisplay), {value: null,})
const surfInput = Inputs.select([null].concat(surfOptions), {value: null,})
const surf = Generators.input(surfInput);

const permStatusInput = Inputs.select([null].concat(["P", "S"]), {value: "P"})
const permStatus = Generators.input(permStatusInput);

// Définition des options d'affichage
const natOptionsDisplay = [
  "04 - Fabrication, production",
  "09 - Commerce de gros",
  "10 - Commerce de détail en magasin",
  "14 - Bâtiment, travaux publics",
  "16 - Commerce de détail sur marché",
  "17 - Commerce de détail sur internet",
  "20 - Location de logements",
  "21 - Location de terrains et autres biens immobiliers",
  "22 - Promotion immobilière de bureaux",
  "23 - Promotion immobilière de logements",
  "24 - Promotion immobilière d'autres bâtiments",
  "25 - Réalisation de programme de construction",
  "26 - Support de patrimoine familial immobilier sans activité de location",
  "99 - Autre"
];
// Extraction des identifiants (ex: "04", "09", "10", etc.)
const natOptions = natOptionsDisplay.map(natOptionsDisplay => natOptionsDisplay.split(" - ")[0]);
// Création du menu déroulant avec affichage complet
const natInputDisplay = Inputs.select([null].concat(natOptionsDisplay), { value: null });
// Création du menu déroulant avec seulement les identifiants
const natInput = Inputs.select([null].concat(natOptions), { value: null });
// Générateur pour récupérer la valeur sélectionnée dynamiquement (uniquement l'identifiant)
const nat = Generators.input(natInput);

const otherNatureActivityInput = Inputs.text({width: width/2, placeholder: "Détaillez une autre nature d'activité si nécessaire"})
const otherNatureActivity = Generators.input(otherNatureActivityInput);

const precActivSecAgriInput = Inputs.text({width: width/2, placeholder: "Détaillez une activité secondaire agricole"})
const precActivSecAgri = Generators.input(precActivSecAgriInput);


```

```js
function transformToUrl(description, options = {}) {
  const baseUrl = "https://codification-meta-rev2-dev.lab.sspcloud.fr/predict?";
  const params = [];
  
  const {
    other_nat = '',
    act_sec_agri = '',
    type_form = '',
    nat = '',
    surf = '',
    cj = '',
    perm_status = '',
    topK = 5
  } = options;

  params.push(`description_activity=${encodeURIComponent(description)}`);

  if (other_nat) params.push(`other_nature_activity=${encodeURIComponent(other_nat)}`);
  if (act_sec_agri) params.push(`precision_act_sec_agricole=${encodeURIComponent(act_sec_agri)}`);
  if (type_form) params.push(`type_form=${encodeURIComponent(type_form)}`);
  if (nat) params.push(`nature=${encodeURIComponent(nat)}`);
  if (surf) params.push(`surface=${encodeURIComponent(surf)}`);
  if (cj) params.push(`cj=${encodeURIComponent(cj)}`);
  if (perm_status) params.push(`activity_permanence_status=${encodeURIComponent(perm_status)}`);
  
  params.push('prob_min=0.0');
  params.push(`top_k=${topK}`);
  
  return baseUrl + params.join('&');
}
```

```js
const urlApe = transformToUrl(activity, {
  top_k: 3, 
  other_nat: otherNatureActivity,
  act_sec_agri: precActivSecAgri,
  type_form: typeForm,
  nat: nat,
  surf: surf,
  cj: cj,
  perm_status:permStatus,
})
```

```js
const predictions = d3.json(urlApe)
```

```js
const predictions_arr = Object.values(predictions)
```

```js
await visibility(); // wait until this node is visible

const context = canvas.getContext("2d");
const start = performance.now();
const duration =2500;

const getColors = d3.scaleSequential(d3.interpolateRdYlGn).domain([0,1])

let frame = requestAnimationFrame(function tick(now) {
  // Clear the canvas first
  context.clearRect(0, 0, canvas.width, canvas.height);
  
  const t = Math.min(predictions_arr.at(-1), (now - start) / duration);
  const barWidth = t * canvas.width;
  
  // Draw the bar
  context.fillStyle = getColors(t);
  context.fillRect(0, 0, barWidth, canvas.height);
  
  // Setup text style
  context.fillStyle = 'white';
  context.font = '20px Arial';
  context.textAlign = 'left';
  context.textBaseline = 'middle';
  
  // Display the value
  const text = `${(t * 100).toFixed(2)}%`;
  const padding = 5; // Padding from the end of the bar
  const textX = Math.min(barWidth + padding, canvas.width - context.measureText(text).width - padding);
  const textY = canvas.height / 2;
  
  context.fillText(text, textX, textY);
  
  if (t < predictions_arr.at(-1)) frame = requestAnimationFrame(tick);
});
```


<!-- ```js
function createResponsiveProgressBar(canvas, predictions_arr) {
  // Make canvas responsive
  function resizeCanvas() {
    const containerWidth = canvas.parentElement.clientWidth;
    canvas.width = Math.min(10000, containerWidth); // max width of 640, or container width if smaller
  }

  // Initial resize
  resizeCanvas();

  // Add resize listener
  window.addEventListener('resize', resizeCanvas);

  const context = canvas.getContext("2d");
  const start = performance.now();
  const duration = 2500;

  const getColors = d3.scaleSequential(d3.interpolateRdYlGn).domain([0,1]);

  let frame = requestAnimationFrame(function tick(now) {
    // Clear the canvas first
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    const t = Math.min(predictions_arr.at(-1), (now - start) / duration);
    const barWidth = t * canvas.width;
    
    // Draw the bar
    context.fillStyle = getColors(t);
    context.fillRect(0, 0, barWidth, canvas.height);
    
    // Setup text style
    context.fillStyle = 'white';
    context.font = '100px Arial';
    context.textAlign = 'left';
    context.textBaseline = 'middle';
    
    // Display the value
    const text = `${(t * 100).toFixed(2)}%`;
    const padding = 5;
    // const textX = Math.min(barWidth + padding, canvas.width - context.measureText(text).width - padding);
    const textX = Math.min(
  barWidth + padding - (t >= 0.7 ? 50 : 0),canvas.width - context.measureText(text).width - padding);
    const textY = canvas.height / 2;
    
    context.fillText(text, textX, textY);
    
    if (t < predictions_arr.at(-1)) frame = requestAnimationFrame(tick);
  });

  // Clean up
  return () => {
    window.removeEventListener('resize', resizeCanvas);
    cancelAnimationFrame(frame);
  };
}

// Usage:
createResponsiveProgressBar(canvas, predictions_arr);
``` -->





<!-- ```js
plot_bar_participants = Plot.plot({
  height: 40,
  marginLeft: 60,
  x: {label: "Indice de confiance →", domain: [0, 1]},
  y: {label: null},
  color: {
    scheme: "ylorrd",
    domain: [0, 1] 
    },
  marks: [
    Plot.barX(current_bar, {x: 1, inset: 0.5, fill: (d) => d}),
  ]
})
``` -->

<style>
    h1.results {
       font-size: 350%;
}
</style>
