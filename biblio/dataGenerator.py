# coding: utf-8
import random
import json
from math import *

sortie = "y",
entree = "x"
minVal =  0
maxVal =  100
fonction =  "cos(cos(4*x*x)+sin(x-3))"
dataSet =[]
dataSet2 =[]
dataLen =  1000

param =  []
for j in range(0,dataLen):
    param.append(random.uniform(minVal, maxVal))
param = sorted(param)
out =  []
for i in param:
    chaine = fonction.replace(entree, str(i))
    dataSet.append({'x':i,'y':eval(chaine)})
    dataSet2.append({'in':i,'out':eval(chaine)})

with open('dataSet/dataset.json', 'w') as f:
    f.write(json.dumps(dataSet))

with open('dataSet/dataset2D.json', 'w') as f:
    donnees  = {"dataSet":dataSet2, "equation":fonction}
    f.write(json.dumps(donnees))


    


