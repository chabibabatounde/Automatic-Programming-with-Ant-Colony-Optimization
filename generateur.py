# coding: utf-8
import sys
import json
from math import *



nomFichier =  "eq8"
inputList = [-1, -10, - 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
chaine =  "(t*t)+exp((t*t)-2) - 6"
sortieChaine =  {"equation":chaine}
diction = []
for sets in inputList:
    diction.append({"in":sets, "out":eval(chaine.replace("t", str(sets)))})
sortieChaine['dataSet'] = diction

f = open("Dataset/"+nomFichier+".json", "a+")
f.write(json.dumps(sortieChaine))
f.close()