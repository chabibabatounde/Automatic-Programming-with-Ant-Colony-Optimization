# coding: utf-8
import random
import networkx as nx
import matplotlib.pyplot as plt
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
#sys.setrecursionlimit(5)


#Charger les données sources
with open("Dataset/eq1.json", 'r') as f:
    dataSet = json.load(f)


#Initialisation des parametres de l'algorithme
nbFourmis =  100
nbGeneration = 10
alpha = 0.1
fonctionSet = [Addition(), Multiplication(), Soustration()]
terminalSet = [Variable('x'),Constante(2),Constante(4)]

#On créé le graph
graphe = nx.Graph()
grapheNodes = []
grapheEdges = []
labeldict = {}
idNode = 0

#on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
nbTerminal = 20
nbFonction = 10


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
    #Pour chaque Noeud, on génère au moins 2 différents arretes et au plus nombreDeNoeud arretes
    nbArrete = random.randint(3, len(grapheNodes))
    for j in range(0, nbArrete):
        #On génère un voisin différent du noeud courant
        voisinId =  random.randint(0, len(grapheNodes)-1)
        while voisinId == currentNodeId :
            voisinId =  random.randint(0, len(grapheNodes)-1)
        edge = (currentNodeId, voisinId, {'pheromone' : 0.05})
        grapheEdges.append(edge)

graphe.add_edges_from(grapheEdges)
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
        arbre , lesChemins,  idNoeudArbre = exploration(fourmi, idNoeudArbre, arbre, labeldict, localGraphe, lesChemins)
        expressionLitterale = parcourir(0, arbre)
        fitness = rawFitness(dataSet, expressionLitterale, 'x')
        #Mise A jour Locale des phéromone
        localGraphe =  miseAJour(localGraphe, lesChemins, fitness, alpha)
        solutionsLocales.append({"expression":expressionLitterale, "fitness":fitness})

    print("\tMeilleure solution : "+expressionLitterale+" => "+str(fitness))
    #Mise A jour globale des phéromone
    graphe =  miseAJour(graphe, lesChemins, fitness, alpha)



#============================================================================================================================================================================================
#============================================================================================================================================================================================
#============================================================================================================================================================================================