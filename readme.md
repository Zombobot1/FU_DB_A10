##Readme

Project done by Esra, Alik and Simon

[Models](https://drive.google.com/file/d/1-lFP6gt_kZZtQuK9rrDhi10YVvghdmDc/view?usp=sharing)

# Installation
**Install poetry & poethepoet**

MacOS, Linux: 

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

Windows:
 
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
    
Both:

    pip install poethepoet

**Create a virtual environment**

    # cd FU_DB_A10
    poetry env use python
    # copy path to the interpreter for PyCharm 
    poetry env info
    
**Install packages**

    # cd FU_DB_A10
    poetry shell
    poetry install
    
# Interactions
1. Launch jupyter notebook **poe notebook**
2. Launch Dash server **poe start**