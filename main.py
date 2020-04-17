# coding: utf-8
import random
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import datetime


from Fonctions.Addition import *
from Fonctions.Multiplication import *
from Fonctions.Soustration import *
from Terminaux.Constante import *
from Terminaux.Variable import *
from Fourmis import *
from exploration import *
from math import *
import json
import sys
#sys.setrecursionlimit(900000000)
'''
chaine =  "((x-(((2+2)-(x+(x+x)))+x))+((x*x)+(x*x)))"
print(eval(chaine.replace("x", str(0))))
'''
#Charger les données sources
with open("Dataset/eq1.json", 'r') as f:
    dataSet = json.load(f)


#Initialisation des parametres de l'algorithme
nbFourmis =  1000
nbGeneration = 100
alpha = 0.1
fonctionSet = [Addition(), Multiplication(), Soustration()]
terminalSet = [Constante('x'),Constante(1),Constante(2),Constante(3),Constante(4),Constante('x')]

#On créé le graph
graphe = nx.Graph()
grapheNodes = []
labeldict = {}
idNode = 0

#on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
nbTerminal = 3
nbFonction = 7


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
plt.savefig("graphe.png")
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
    for i in range(0, 4):
        solution  = solutionsLocales[i]
        solutionsGenerales.append(solution)
        #Mise A jour globale des phéromone apres chaque génération (4 meilleurs de la génération)
        graphe =  miseAJour(graphe, solution['lesChemins'], solution['fitness'], alpha)
    print("\t Meilleure solution : "+ solutionsLocales[0]['expression'] + " [Fitness = "+str(solutionsLocales[0]['fitness']))+"]"
    


solutionsGenerales =  sorted(solutionsGenerales, key=itemgetter('fitness'))
print("=========================================================================================================================")
print("SOLUTION : "+ solutionsGenerales[0]['expression'] + " [Fitness = "+str(solutionsGenerales[0]['fitness'])+"]")


laDate = datetime.datetime.now()
logDate = None
logData["date"] =  str(laDate.hour) + ":" +str(laDate.minute) + ":" +str(laDate.second)+" "+str(laDate.day) + "-" +str(laDate.month) + "-" +str(laDate.year)






#============================================================================================================================================================================================
#============================================================================================================================================================================================
#============================================================================================================================================================================================eval