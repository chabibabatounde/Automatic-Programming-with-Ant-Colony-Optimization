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
#sys.setrecursionlimit(5000000)

#Chargement de la dataSet
with open("Dataset/eq1.json", 'r') as f:
    dataSet = json.load(f)


#Initialisation des parametres de l'algorithme
nbFourmis =  10
nbGeneration = 1
evaporation = 0.01
fonctionSet = [Addition(), Multiplication(), Soustration()]
terminalSet = [Variable('x'),Constante(2),Constante(4)]
graphe = nx.Graph()
grapheNodes = []
grapheEdges = []
labeldict = {}
idNode = 0

#On génére le graphe
for fonction in fonctionSet:
    graphe.add_node(idNode, value=fonction)
    grapheNodes.append(fonction)
    labeldict[idNode] = fonction.valeur
    idNode = idNode +1
for terminal in terminalSet:
    graphe.add_node(idNode, value=terminal)
    grapheNodes.append(terminal)
    labeldict[idNode] = terminal.valeur
    idNode = idNode +1
for i in range(len(grapheNodes)):
    for j in range(len(grapheNodes)):
        if(i != j ):
            edge = (i, j, {'pheromone' : 0.5})
            grapheEdges.append(edge)
graphe.add_edges_from(grapheEdges)
nx.draw(graphe, labels=labeldict, with_labels = True)
plt.savefig("graphe.png") # save as png
#plt.show() # display'''
plt.clf()



#============================================================================================================================================================================================
#============================================================================================================================================================================================
#Pour chaque génération
for generation in range(0, nbGeneration):
    print("Génération "+str(generation+1))
    #Déterminer un point de démarrage
    noeudDemarrage = random.randint(0, len(grapheNodes)-1)
    noeudCourant = grapheNodes[noeudDemarrage]
    while not (isFunction(noeudCourant)):
        noeudDemarrage = random.randint(0, len(grapheNodes)-1)
        noeudCourant = grapheNodes[noeudDemarrage]
    
    for f in range(0, nbFourmis):
        #Pour chaque fourmi alors
        #Initialiser l'arbre du programme
        labeldict = {}
        arbre = nx.Graph()
        #Initialiser le tableau des noeuds et des arretes
        arbreNodes = []
        arbreEdges = []
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
    '''fourmiGeneratrice = Fourmis(noeudDemarrage, noeudDemarrage,  0)
    arbre, lesChemins, idNoeudArbre = exploration(fourmiGeneratrice, 1, arbre, labeldict, graphe, lesChemins)
    nx.draw(arbre, labels=labeldict, with_labels = True)
    plt.savefig("arbre.png") # save as png'''
    #plt.show() # display


    '''  expression = construire(graphe, grapheNodes, noeudDemarrage)
    fitness = rawFitness(dataSet, expression, 'x')
    print("\t================================================================================")
    print("\t SOLUTION "+str(f+1)+" : "+expression+" => "+str(fitness))'''


#============================================================================================================================================================================================
#============================================================================================================================================================================================
#============================================================================================================================================================================================