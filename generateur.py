# coding: utf-8
import sys
import json
from math import *



nomFichier =  "eq6"
inputList = [-1, -10, - 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
chaine =  "(3*x)+4"
sortieChaine =  {"equation":chaine}
diction = []
for sets in inputList:
    diction.append({"in":sets, "out":eval(chaine.replace("x", str(sets)))})
sortieChaine['dataSet'] = diction

f = open("Dataset/"+nomFichier+".json", "a+")
f.write(json.dumps(sortieChaine))
f.close()