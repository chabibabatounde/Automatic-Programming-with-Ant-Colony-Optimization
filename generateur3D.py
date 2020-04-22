# coding: utf-8
import sys
import json
from math import *



nomFichier =  "sys5"
inputList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
chaine1 =  "t-3"
chaine2 =  "t"
chaine3 =  "t*t"
sortieChaine = {}
sortieChaine["systeme"] =  {"equation1":chaine1, "equation2":chaine2, "equation3":chaine3}
diction = []
for sets in inputList:
    a=eval(chaine1.replace("t", str(sets)))
    b=eval(chaine2.replace("t", str(sets)))
    c=eval(chaine3.replace("t", str(sets)))

    diction.append({"t":sets, "x":a, "y":eval(str(a)+"*"+str(b)), "z":eval(str(b)+"+"+str(c))})
    
    #diction.append({"t":sets, "x":eval(chaine1.replace("t", str(sets))), "y":eval(chaine2.replace("t", str(sets))), "z":eval(chaine3.replace("t", str(sets)))})
sortieChaine['dataSet'] = diction

f = open("Dataset/3D/"+nomFichier+".json", "a+")
f.write(json.dumps(sortieChaine))
f.close()