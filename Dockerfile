ARG BASE_IMAGE=inseefrlab/onyxia-python-datascience
FROM $BASE_IMAGE

USER root

# Clone repository
RUN git clone https://github.com/InseeFrLab/codif-ape-dashboard.git .

RUN pip3 install -r requirements.txt

RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.489/quarto-1.4.489-linux-amd64.deb -O quarto.deb \
    sudo dpkg -i quarto.deb \
    quarto check install \
    rm quarto.deb

RUN quarto render --output-dir _build

ENTRYPOINT ["shiny", "run", "_build/app.py"]
