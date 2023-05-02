#!/bin/bash
# ambiente virtual para instalar coisas
python3 -m venv .
# pip sempre desatualizado por alguma razao
pip install --upgrade pip
# entrar no ambiente virtual
source bin/activate
# instalar pacotes
pip install opencv-python
pip install numpy
python3 execute.py
