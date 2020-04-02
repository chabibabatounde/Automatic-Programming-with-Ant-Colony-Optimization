# coding: utf-8
import random
import networkx as nx
import matplotlib.pyplot as plt
from Fonctions.Addition import *
from Fonctions.Soustration import *
from Fonctions.Multiplication import *
from Fonctions.Cos import *
from Fonctions.Sin import *
from Fonctions.Sqrt import *
from Terminaux.Constante import *
from Terminaux.Variable import *
from Fourmis import *
from exploration import *
from networkx.readwrite import json_graph

# 2x² + 4x - 9
#Initialisation des parametres de l'algorithme
nbFourmis =  1
nbGeneration = 1
fonctionSet = [Addition(), Multiplication(), Cos()]
terminalSet = [Variable("x"),Constante(2),Constante(4),]
alpha = 0.1

#============================================================================================================================================================================================
#============================================================================================================================================================================================
#============================================================================================================================================================================================

#On créé le graph
graphe = nx.Graph()
grapheNodes = []
grapheEdges = []
idNode = 0

#on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
nbTerminal = 10
nbFonction = 10


labeldict = {}

#On génére de manière aléatoire les éléments du graphe
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
        edge = (currentNodeId, voisinId, {'pheromone' : 0.5})
        grapheEdges.append(edge)

graphe.add_edges_from(grapheEdges)
nx.draw(graphe, labels=labeldict, with_labels = True)
plt.savefig("graphe.png") # save as png
#plt.show() # display'''
plt.clf()

#=======================DEMARAGE DE LA ROUTINE DE L'ALGO=====================
#Démarrage de l'algorithme

#Pour chaque génération
for generation in range(0, nbGeneration):
    #Pour chaque fourmi alors
    #Déterminer un point de démarrage
    idNoeudCourant = random.randint(0, len(grapheNodes)-1)
    noeudCourant = grapheNodes[idNoeudCourant]
    while not (isFunction(noeudCourant)):
        idNoeudCourant = random.randint(0, len(grapheNodes)-1)
        noeudCourant = grapheNodes[idNoeudCourant]
    for f in range(0, nbFourmis):
        #Initialiser l'arbre du programme
        labeldict = {}
        arbre = nx.Graph()
        #arbre = nx.DiGraph()
        #Initialiser le tableau des noeuds et des arretes
        arbreNodes = []
        arbreEdges = []
        ''' SI PREMIERE FOURMI DE LA PREMIERE GENERATION '''
        #Initialisation de l'identifiant des noeuds
        idNoeudArbre = 0
        #Ajout du de départ dans la liste des noeuds
        arbre.add_node(idNoeudArbre, value=noeudCourant)
        labeldict[idNoeudArbre] = noeudCourant.valeur
        #Création d'une fourmi avec les données
        fourmi = Fourmis(idNoeudCourant, idNoeudCourant,  idNoeudArbre)
        #On incrémente l'identifiant des noeuds
        idNoeudArbre =  idNoeudArbre + 1
        #==================== EXPLORATION ====================#
        arbre , idNoeudArbre = exploration(fourmi, idNoeudArbre, arbre, labeldict, graphe)
        expressionLitterale = parcourir(arbre)

        nx.draw(arbre, labels=labeldict, with_labels = True)
        plt.savefig("arbre.png") # save as png
        plt.show() # display'''
#============================================================================================================================================================================================
#============================================================================================================================================================================================
#============================================================================================================================================================================================