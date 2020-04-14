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
nbFourmis =  10
nbGeneration = 1
evaporation = 0.01
fonctionSet = [Addition(), Multiplication(), Soustration()]
terminalSet = [Variable('x'),Constante(2),Constante(4)]

#On créé le graph
graphe = nx.Graph()
grapheNodes = []
grapheEdges = []
labeldict = {}
idNode = 0

#on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
nbTerminal = 9
nbFonction = 6



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
        edge = (currentNodeId, voisinId, {'pheromone' : 0.5})
        grapheEdges.append(edge)

graphe.add_edges_from(grapheEdges)
nx.draw(graphe, labels=labeldict, with_labels = True)
plt.savefig("graphe.png")
plt.clf()


#=======================DEMARAGE DE LA ROUTINE DE L'ALGO=====================
#Démarrage de l'algorithme
#Pour chaque génération
for generation in range(0, nbGeneration):
    print("Génération "+str(generation+1))
    
    #Pour chaque fourmi alors
    #Déterminer un point de démarrage
    idNoeudCourant = random.randint(0, len(grapheNodes)-1)
    noeudCourant = grapheNodes[idNoeudCourant]
    while not (isFunction(noeudCourant)):
        idNoeudCourant = random.randint(0, len(grapheNodes)-1)
        noeudCourant = grapheNodes[idNoeudCourant]
    noeudDemarrage = idNoeudCourant
    
    for f in range(0, nbFourmis):
        #Initialiser l'arbre du programme
        labeldict = {}
        arbre = nx.Graph()
        
        #arbre = nx.DiGraph()
        #Initialiser le tableau des noeuds et des arretes
        arbreNodes = []
        arbreEdges = []
        #Initialisation de l'identifiant des noeuds
        idNoeudArbre = 0
        #Ajout du de départ dans la liste des noeuds
        arbre.add_node(idNoeudArbre, value=noeudCourant)
        labeldict[idNoeudArbre] = noeudCourant.valeur
        #Création d'une fourmi avec les données
        fourmi = Fourmis(idNoeudCourant, idNoeudCourant,  idNoeudArbre)
        #On incrémente l'identifiant des noeuds
        idNoeudArbre =  idNoeudArbre + 1
        #Initialisation du tableau des chemins parcourus
        lesChemins = []
        #==================== EXPLORATION ====================#
        arbre , lesChemins,  idNoeudArbre = exploration(fourmi, idNoeudArbre, arbre, labeldict, graphe, lesChemins)

        
        expressionLitterale = parcourir(0, arbre)

        fitness = rawFitness(dataSet, expressionLitterale, 'x')
        alpha = adjustedFitness(fitness)
        print("\t Fourmi "+str(f+1)+" : "+expressionLitterale+" => "+str(fitness)+" => "+str(alpha))
        #Mise à jour des phéromones
            #Incrémentation
        for chemin in lesChemins:
            graphe[chemin[0]][chemin[1]]['pheromone'] = graphe[chemin[0]][chemin[1]]['pheromone'] + alpha
        
        #evaporation
        for lignes in graphe.edges():
            graphe[lignes[0]][lignes[1]]['pheromone'] = graphe[lignes[0]][lignes[1]]['pheromone'] - evaporation
    
        #   RESULTAT   #
    #============================
        #expressionLitterale
        #fitness
    #============================
    #decrire(graphe)
    
    #plt.show() # display
    

    expression = construire(graphe, grapheNodes, noeudDemarrage)
    fitness = rawFitness(dataSet, expression, 'x')
    print("\t================================================================================")
    print("\t SOLUTION "+str(f+1)+" : "+expression+" => "+str(fitness))


#============================================================================================================================================================================================
#============================================================================================================================================================================================
#============================================================================================================================================================================================