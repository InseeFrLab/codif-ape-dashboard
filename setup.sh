#!/bin/bash
git config --global credential.helper store

pip install -r requirements.txt
pip install pre-commit
pre-commit install

AWS_ACCESS_KEY_ID=`vault kv get -field=ACCESS_KEY onyxia-kv/projet-ape/s3` && export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=`vault kv get -field=SECRET_KEY onyxia-kv/projet-ape/s3` && export AWS_SECRET_ACCESS_KEY

wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.489/quarto-1.4.489-linux-amd64.deb -O quarto.deb
sudo dpkg -i quarto.deb
quarto check install
rm quarto.deb
