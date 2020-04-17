# coding: utf-8
import sys
import random
import json
from math import *
import datetime

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D


from Fonctions.Addition import *
from Fonctions.Multiplication import *
from Fonctions.Soustration import *
from Fonctions.Cos import *
from Fonctions.Sin import *

from Terminaux.Constante import *
from Terminaux.Variable import *

from Fourmis import *
from exploration import *
#sys.setrecursionlimit(900000000)

laDate = datetime.datetime.now()

'''
chaine =  "cos(x-2)"
print(eval(chaine.replace("x", str(0))))ss
'''

#Charger les données sources
nomFichier = "eq1"

with open("Dataset/"+nomFichier+".json", 'r') as f:
    ressource = json.load(f)
    dataSet = ressource["dataSet"]




#Initialisation des parametres de l'algorithme
nbFourmis =  100
nbGeneration = 100
alpha = 0.1
fonctionSet = [Addition(), Multiplication(),Soustration()]
terminalSet = [Constante('x'),Constante(1),Constante(2),Constante(3),Constante(4),Constante('x')]

#On créé le graph
graphe = nx.Graph()
grapheNodes = []
labeldict = {}
idNode = 0

#on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
nbTerminal = 6
nbFonction = 14

#On génére le graphe de maniere unique
for i in range(0, nbFonction):
    nodeToAdd = fonctionSet[random.randint(0, len(fonctionSet) - 1)]
    graphe.add_node(idNode, value=nodeToAdd)
    grapheNodes.append(nodeToAdd)
    labeldict[idNode] = nodeToAdd.valeur
    idNode = idNode +1
for i in range(0, nbTerminal):
    nodeToAdd = terminalSet[random.randint(0, len(terminalSet) - 1)]
    graphe.add_node(idNode, value=nodeToAdd)
    grapheNodes.append(nodeToAdd)
    labeldict[idNode] = nodeToAdd.valeur
    idNode = idNode +1

#Génération des arretes
for currentNodeId in range(len(grapheNodes)):
    currentNode = grapheNodes[currentNodeId]
    voisins =  list(graphe.neighbors(currentNodeId))
    #Pour chaque Noeud, on génère au moins 3 différents arretes et au plus nombreDeNoeud arretes
    nbArrete = random.randint(3, len(grapheNodes))
    for j in range(0, nbArrete):
        #On génère un voisin différent du noeud courant
        voisinId =  random.randint(0, len(grapheNodes)-1)
        while voisinId == currentNodeId :
            voisinId =  random.randint(0, len(grapheNodes)-1)
        graphe.add_edge(currentNodeId, voisinId, pheromone= 0.05)

nx.draw(graphe, labels=labeldict, with_labels = True)
plt.savefig("Sortie/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+"-graphe.png")
plt.clf()

#=======================DEMARAGE DE LA ROUTINE DE L'ALGO=====================
#Déterminer un point de démarrage
noeudDemarrage = random.randint(0, len(grapheNodes)-1)
noeudCourant = grapheNodes[noeudDemarrage]

while not (isFunction(noeudCourant)):
    noeudDemarrage = random.randint(0, len(grapheNodes)-1)
    noeudCourant = grapheNodes[noeudDemarrage]
    #noeudDemarrage = idNoeudCourant

#Pour chaque génération
solutionsGenerales = []
metriqueEvolutions = []
for generation in range(0, nbGeneration):
    print("Génération "+str(generation+1))
    localGraphe = graphe
    solutionsLocales = []
    #Pour chaque fourmi alors
    for f in range(0, nbFourmis):
        #Choix du noeud suivant
        idSuivant = noeudSuivant(noeudDemarrage, localGraphe)
        #Initialiser l'arbre du programme
        labeldict = {}
        arbre = nx.Graph()
        #Initialisation de l'identifiant des noeuds
        idNoeudArbre = 0
        #Ajout du de départ dans la liste des noeuds
        arbre.add_node(idNoeudArbre, value=noeudCourant)
        labeldict[idNoeudArbre] = noeudCourant.valeur
        #Création d'une fourmi avec les données
        fourmi = Fourmis(noeudDemarrage, noeudDemarrage,  idNoeudArbre)
        #On incrémente l'identifiant des noeuds
        idNoeudArbre =  idNoeudArbre + 1
        #Initialisation du tableau des chemins parcourus
        lesChemins = []
        arbre , lesChemins,  idNoeudArbre, maxFn = exploration(fourmi, idNoeudArbre, arbre, labeldict, localGraphe, lesChemins, 10)
        expressionLitterale = parcourir(0, arbre)
        fitness = rawFitness(dataSet, expressionLitterale, 'x')
        solutionsLocales.append({"expression":expressionLitterale, "fitness":fitness, "lesChemins":lesChemins})
        #Mise A jour Locale des phéromone
        localGraphe =  miseAJour(localGraphe, lesChemins, fitness, alpha)

    solutionsLocales =  sorted(solutionsLocales, key=itemgetter('fitness'))
    for i in range(0, 10):
        solution  = solutionsLocales[i]
        
        #Mise A jour globale des phéromone apres chaque génération (4 meilleurs de la génération)
        graphe =  miseAJour(graphe, solution['lesChemins'], solution['fitness'], alpha)
    print("\t Meilleure solution : "+ solutionsLocales[0]['expression'] + " [Fitness = "+str(solutionsLocales[0]['fitness']))+"]"
    solutionsGenerales.append(solutionsLocales[0])
    
#====================   Affichage de la solution   =========================#

generation = 0
performx = []
performy = []
for ln in solutionsGenerales:
    generation = generation +1
    performx.append(ln['fitness'])
    performy.append(generation)

plt.plot(performy, performx, label="Evolution de fitness suivant les generation de fourmis")
plt.legend()
plt.savefig("Sortie/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+".evolution.png", dpi=500)
plt.clf()





solutionsGenerales =  sorted(solutionsGenerales, key=itemgetter('fitness'))
print("=========================================================================================================================")
print("SOLUTION : "+ solutionsGenerales[0]['expression'] + " [Fitness = "+str(solutionsGenerales[0]['fitness'])+"]")


#====================   Journalisation   =========================#
logData = {}
logData["alpha"] = alpha
if(solutionsGenerales[0]['fitness']==0 or solutionsGenerales[0]['fitness']==1):
    logData["trouve"] = 1
else:
    logData["trouve"] = 0
logData["equation"] = ressource["equation"]
logData["date"] =  str(laDate.hour) + ":" +str(laDate.minute) + ":" +str(laDate.second)+" "+str(laDate.year) + "-" +str(laDate.month) + "-" +str(laDate.day)
logData["nbFonction"] = nbFonction
logData["nbTerminal"] = nbTerminal
logData["nbFourmis"] = nbFonction
logData["nbGeneration"] = nbGeneration
logData["minFitness"] = solutionsGenerales[0]['fitness']
logData["minExpression"] = solutionsGenerales[0]['expression']
logData["maxFitness"] = solutionsGenerales[len(solutionsGenerales)-1]['fitness']
logData["maxExpression"] = solutionsGenerales[len(solutionsGenerales)-1]['expression']
f = open("Sortie/log/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+".json", "a")
f.write(json.dumps(logData))
f.close()

x = []
y = []

x1 = []
y1 = []

x2 = []
y2 = []


for ligne in dataSet:
    chaine =  logData["minExpression"]
    chaine2 =  logData["maxExpression"]

    x.append(ligne['in'])
    y.append(ligne['out'])


    x1.append(ligne['in'])
    y1.append(eval(chaine.replace("x", str(ligne['in']))))

    x2.append(ligne['in'])
    y2.append(eval(chaine2.replace("x", str(ligne['in']))))


plt.plot(x, y, label="Dataset")
plt.legend()
plt.savefig("Sortie/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+".dataset.png", dpi=500)

plt.plot(x1, y1, label="Solution")
plt.legend()
plt.savefig("Sortie/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+".solution.png", dpi=500)
'''
plt.plot(x2, y2, label="Last solution")
plt.legend()
plt.savefig("Sortie/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+".results.png", dpi=500)
'''
plt.show()
print(len(solutionsGenerales))