ARG BASE_IMAGE=inseefrlab/onyxia-python-datascience
FROM $BASE_IMAGE

USER root

# Set environment
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ARG AWS_S3_ENDPOINT
ENV AWS_S3_ENDPOINT=${AWS_S3_ENDPOINT}

WORKDIR /app

# Clone repository
RUN git clone https://github.com/InseeFrLab/codif-ape-dashboard.git .

RUN pip3 install -r requirements.txt

RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.489/quarto-1.4.489-linux-amd64.deb -O quarto.deb &&\
    sudo dpkg -i quarto.deb &&\
    quarto check install &&\
    rm quarto.deb

RUN echo $AWS_ACCESS_KEY_ID

RUN echo $AWS_SECRET_ACCESS_KEY

RUN echo $AWS_S3_ENDPOINT

RUN quarto render --output-dir _build

ENTRYPOINT ["shiny", "run", "_build/app.py"]
