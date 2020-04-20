# coding: utf-8
import sys
import json
from math import *



nomFichier =  "sys1"
inputList = [-1, -10, - 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
chaine1 =  "cos(t-1)"
chaine2 =  "2*t*t"
chaine3 =  "t+7"
sortieChaine = {}
sortieChaine["systeme"] =  {"equation1":chaine1, "equation2":chaine2, "equation3":chaine3}
diction = []
for sets in inputList:
    diction.append({"t":sets, "x":eval(chaine1.replace("t", str(sets))), "y":eval(chaine2.replace("t", str(sets))), "z":eval(chaine3.replace("t", str(sets)))})
sortieChaine['dataSet'] = diction

f = open("Dataset/"+nomFichier+".json", "a+")
f.write(json.dumps(sortieChaine))
f.close()