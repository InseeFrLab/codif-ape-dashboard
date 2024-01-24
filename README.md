# NACE (rev 2.1) Monitoring Dashboard 📊

We provide all the necessary code to create a dashboard for monitoring the APE classification model. This repository is equipped with the tools to visualize model performance, enabling seamless monitoring and decision-making. The dashboard, powered by Quarto's new features, allows users to track key metrics, visualize predictions, and make informed decisions based on quasi-real-time data. The dashboard can be accessed at [https://dashboard-ape.lab.sspcloud.fr/](https://dashboard-ape.lab.sspcloud.fr/).

## Prerequisites

- Python 3.10
- Python libraries: see `requirements.txt`
- Quarto > 1.4

## Development

To develop the dashboard, install the dependencies (`pip install -r requirements.txt` and `. setup.sh`), then modify the `index.qmd` file. Launch the dashboard locally with the command `quarto serve index.qmd`.

## License

This project is under the [Apache license](https://github.com/InseeFrLab/codif-ape-train/blob/main/LICENSE) to encourage collaboration and free use.
