// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Codification APE RIAS/SSP Lab",


  pages: [
    {name: "Performance du modèle", path: "/performance"},
    {name: "Surveillance automatisée du modèle", path: "/surveillance-auto"},
    {name: "Explicabilité", path: "/explainability"},
    {name: "Changement de nomenclature NAF 2025", path: "/naf-2025"},
    {name: "Codification en NAF rev 2", path: "/naf-rev2"}
  ],

  // Content to add to the head of the page, e.g. for a favicon:
  head: '<link rel="icon" href="favicon-onyxia.png" type="image/png" sizes="32x32">',

  // The path to the source root.
  root: "src",

  // Some additional configuration options and their defaults:
  // theme: "default", // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // sidebar: true, // whether to show the sidebar
  // toc: true, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // cleanUrls: true, // drop .html from URLs
};
