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
from Fonctions.Expo import *
from Fonctions.Sin import *

from Terminaux.Constante import *
from Terminaux.Variable import *

from Fourmis import *
from exploration import *
#sys.setrecursionlimit(900000000)

laDate = datetime.datetime.now()


#Charger les données sources
nomFichier = "sys5"

with open("Dataset/3D/"+nomFichier+".json", 'r') as f:
    ressource = json.load(f)
    dataSet = ressource["dataSet"]
    equations = ressource["systeme"]


#Initialisation des parametres de l'algorithme
nbFourmis =  4
nbGeneration = 4
alpha = random.uniform(0,0.25)
#fonctionSet = [Addition(), Multiplication(),Soustration()]
fonctionSet = [Addition(), Multiplication(), Sin(), Cos(),Soustration()]
terminalSet = [Constante('t'),Constante(1),Constante(2),Constante(3),Constante(4),Constante(5),Constante('t')]



#on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
nbTerminal = 6
nbFonction = 14

tableauVariablesPosition = ['x','y','z']
solutionGlobale = {}
#Pour chaque parametres du parcours
for parametre in tableauVariablesPosition :
    #Préparer le jeu de données sur l'axe
    jeuDeDonnees =  []
    for ligne in dataSet:
        jeuDeDonnees.append(ligne[parametre])

    #On génére un graphe
    graphe = nx.Graph()
    grapheNodes = []
    labeldict = {}
    idNode = 0

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
        nbArrete = random.randint(3, len(grapheNodes)-1)
        for j in range(0, nbArrete):
            #On génère un voisin différent du noeud courant
            voisinId =  random.randint(0, len(grapheNodes)-1)
            while voisinId == currentNodeId :
                voisinId =  random.randint(0, len(grapheNodes)-1)
            graphe.add_edge(currentNodeId, voisinId, p= 0.05)

    nx.draw(graphe, labels=labeldict, with_labels = True)
    #edge_labels=nx.draw_networkx_edge_labels(graphe,pos=nx.spring_layout(graphe))
    plt.savefig("Sortie/3D/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+"-graphe-"+parametre+".png")
    plt.clf()

    #=======================DEMARAGE DE LA ROUTINE DE L'ALGO=====================
    print("\n===> Optimisation sur l'axe "+parametre+" <===")
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
        print("\tGénération "+str(generation+1))
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
            fitness = rawFitness3D(jeuDeDonnees, expressionLitterale, 't')
            solutionsLocales.append({"expression":expressionLitterale, "fitness":fitness, "lesChemins":lesChemins})

        #Calcul du fitness moyen de la génération
        fitnessMoyen =  0
        for ln in solutionsLocales:
            fitnessMoyen = fitnessMoyen + ln['fitness']
        metriqueEvolutions.append(float(fitnessMoyen) / float(len(solutionsLocales)))
        #Trie et choix des meilleures solutions
        solutionsLocales =  sorted(solutionsLocales, key=itemgetter('fitness'))
        for i in range(0, 4):
            solution  = solutionsLocales[i]
            #Mise A jour globale des phéromone apres chaque génération (4 meilleurs de la génération)
            graphe =  miseAJour(graphe, solution['lesChemins'], solution['fitness'], alpha)

        #print("\t\tMeilleure solution : "+ solutionsLocales[0]['expression'] + " [Fitness = "+str(solutionsLocales[0]['fitness']))+"]"
        solutionsGenerales.append(solutionsLocales[0])
        
    solutionsGenerales =  sorted(solutionsGenerales, key=itemgetter('fitness'))

    print("=========================================================================================================================")
    print("SOLUTION sur l'axe "+parametre+": "+ solutionsGenerales[0]['expression'] + " [Fitness = "+str(solutionsGenerales[0]['fitness'])+"]")
    print("=========================================================================================================================")
    solutionGlobale[parametre] =  {'expression':solutionsLocales[0]['expression'], 'fitness':solutionsLocales[0]['expression']} 

plt.clf()

#Tracé en 3D
#data sur x
x = []
xx = []

y = []
yy = []

z = []
zz = []

for ligne in dataSet:
    chaine =  solutionGlobale['x']['expression']
    x.append(eval(chaine.replace("t", str(ligne['x']))))
    xx.append(ligne['x'])

    chaine =  solutionGlobale['y']['expression']
    y.append(eval(chaine.replace("t", str(ligne['y']))))
    yy.append(ligne['y'])

    chaine =  solutionGlobale['z']['expression']
    z.append(eval(chaine.replace("t", str(ligne['z']))))
    zz.append(ligne['z'])



mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')


ax.plot(xx, yy, zz, label="Comportement connu")
ax.plot(x, y, z, label="Comportement obtenu")

ax.legend()
plt.savefig("Sortie/3D/img/"+nomFichier+"-"+str(laDate.year) + str(laDate.month) +str(laDate.day) +"-"+str(laDate.hour) +str(laDate.minute) +str(laDate.second)+"-solution.png", dpi=500)
plt.show()