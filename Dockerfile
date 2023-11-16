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

# Install shiny server
# RUN apt-get update &&\
#     apt-get install -y gdebi-core &&\
#     RUN wget https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.20.1002-amd64.deb &&\
#     RUN gdebi -n shiny-server-1.5.20.1002-amd64.deb

# Custom config
# RUN sed -i '1s/^/python \/usr\/bin\/python3;\n/' /etc/shiny-server/shiny-server.conf

# Install systemd
# RUN apt-get install systemd

WORKDIR /app

# Clone repository
RUN git clone https://github.com/InseeFrLab/codif-ape-dashboard.git .

RUN pip3 install -r requirements.txt

RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.489/quarto-1.4.489-linux-amd64.deb -O quarto.deb &&\
    sudo dpkg -i quarto.deb &&\
    quarto check install &&\
    rm quarto.deb

RUN rm -rf /srv/shiny-server/*

RUN quarto render --output-dir _build/

EXPOSE 80

ENTRYPOINT ["uvicorn", "_build.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
