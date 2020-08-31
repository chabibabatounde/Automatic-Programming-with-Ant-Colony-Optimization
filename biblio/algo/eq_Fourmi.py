# coding: utf-8
import random
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

from mpl_toolkits.mplot3d import Axes3D
from math import *
from Fonctions.Addition import *
from Fonctions.Multiplication import *
from Fonctions.Soustration import *
from Fonctions.Cos import *
from Fonctions.Expo import *
from Fonctions.Sin import *
from Visuleur import * 
from Terminaux.Constante import *
from Terminaux.Variable import *
from Fourmis import *


# coding: utf-8
class eq_Fourmi:
    dataSet = []
    nbIndividu=0
    nbIterration=0
    visualiseur = Visuleur()
    learningRate = 0.95
    variablesSortie = ''
    variablesEntree = []
    trigo =  False
    maxDeep =  10
    
    def run (self):
        alpha = random.uniform(0,0.25)
        fonctionSet = [Addition(),Multiplication(), Soustration()]


        if self.trigo:
            fonctionSet.append(Cos())
            fonctionSet.append(Sin())

        terminalSet = [Constante(1),Constante(2),Constante(3),Constante(4),Constante(5)]
        for variable in self.variablesEntree:
            terminalSet.append(Constante(variable))
            terminalSet.append(Constante(variable))



        #On créé le graph
        graphe = nx.Graph()
        grapheNodes = []
        labeldict = {}
        idNode = 0

        #on defini le nombre de fonctions et de terminaux qu'on veux dans notre graphe
        nbTerminal = 10
        nbFonction = 30

        #On génére le graphe
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

        self.visualiseur.drawGraph(graphe, labeldict)

        #=======================DEMARAGE DE LA ROUTINE DE L'ALGO=====================
        #Déterminer un point de démarrage
        noeudDemarrage = random.randint(0, len(grapheNodes)-1)
        noeudCourant = grapheNodes[noeudDemarrage]

        while not (self.isFunction(noeudCourant)):
            noeudDemarrage = random.randint(0, len(grapheNodes)-1)
            noeudCourant = grapheNodes[noeudDemarrage]
            #noeudDemarrage = idNoeudCourant

        #Pour chaque génération
        solutionsGenerales = []
        for generation in range(0, self.nbIterration):
            print("\t Génération "+str(generation+1))
            localGraphe = graphe
            solutionsLocales = []
            #Pour chaque fourmi alors
            for f in range(0, self.nbIndividu):
                #Choix du noeud suivant
                idSuivant = self.noeudSuivant(noeudDemarrage, localGraphe)
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
                arbre , lesChemins,  idNoeudArbre, maxFn = self.exploration(fourmi, idNoeudArbre, arbre, labeldict, localGraphe, lesChemins, self.maxDeep)
                expressionLitterale = self.parcourir(0, arbre)
                fitness = self.rawFitness(self.dataSet, expressionLitterale)
                solutionsLocales.append({"expression":expressionLitterale, "fitness":fitness, "lesChemins":lesChemins})

            solutionsLocales =  sorted(solutionsLocales, key=itemgetter('fitness'))

            for i in range(0, 5):
                solution  = solutionsLocales[i]
                #Mise A jour globale des phéromone apres chaque génération (4 meilleurs de la génération)
                graphe =  self.miseAJour(graphe, solution['lesChemins'], solution['fitness'], alpha)

            print("\t\t Meilleure solution : "+ solutionsLocales[0]['expression'] + " [Fitness = "+str(solutionsLocales[0]['fitness']))+"]"
            solutionsGenerales.append(solutionsLocales[0])

        solutionsGenerales =  sorted(solutionsGenerales, key=itemgetter('fitness'))
        



        return solutionsGenerales[0]['expression']

    def noeudSuivant(self, idNoeud, graphe):
        qZero = random.uniform(0, 1)
        idSuivant =  idNoeud
        if(qZero > self.learningRate):
            #Choix aléatoire
            voisins = list(graphe.neighbors(idNoeud))
            position  =  random.randint(0, len(voisins)-1)
            idSuivant = voisins[position]
        else:
            #voisins = list(graphe.neighbors(idNoeud))
            voisins = list(graphe.neighbors(idNoeud))
            total = 0
            roulette =  []
            for suivant in voisins:
                total = total + graphe[idNoeud][suivant]['p']
            estqi =  0
            for suivant in voisins:
                proba = round(graphe[idNoeud][suivant]['p'] * 100 / total)
                estqi = estqi + proba
                for j in range(0, int(proba)):
                    roulette.append(suivant)
            choix = random.randint(0, len(roulette)-1)
            idSuivant = roulette[choix]
        return idSuivant

    def rawFitness(self, dataSet, expression):
        fitness =  0
        try:
            for ligne in dataSet:
                for param in self.variablesEntree:
                    expression = expression.replace(param,str(ligne[param]))
                    local = eval(expression)
                    fitness = fitness + abs(local - ligne[self.variablesSortie])
        except:
            print("infinite")
            fitness = float('inf')
        return (fitness+1)

    def miseAJour(self, graphe, lesChemins, fitness, alpha):
        # Renforcement
        for lignes in lesChemins:
            graphe[lignes[0]][lignes[1]]['p'] = graphe[lignes[0]][lignes[1]]['p'] + (float(1) / float(fitness) )
        # Evaporation
        for lignes in graphe.edges():
            graphe[lignes[0]][lignes[1]]['p'] = graphe[lignes[0]][lignes[1]]['p'] * (1 - alpha)
        return graphe

    def parcourir(self, idNoeud, arbre, ancetre=None):
        #sys.setrecursionlimit(10)
        #Récupérer le noeud racine
        racine = arbre.nodes[idNoeud]['value']
        #Initialiser "Expression" à ""
        localExpression = ""
        #Initialiser le tableau des paramêtres à vide
        parametres = []
        #Si c'est une fonction
        if(self.isFunction(racine)):
            #Récupérer les fils
            listDesFils =  list(arbre.neighbors(idNoeud))
            #Pour chaque fils :
            for i in listDesFils:
                #récupérer la valeur
                fils = arbre.nodes[i]['value']
                #Si le noeud est une fonction :
                if self.isFunction(fils):
                    #On vérifie si on ne va pas en arriere
                    if(i != ancetre):
                        sortie = self.parcourir(i, arbre, idNoeud)
                        #Ajouter l'expression dans le tableau des paramêtres
                        parametres.append(sortie)
                #Si le noeud est un terminal
                else :
                    #Ajouter la valeur"dans le tableau des paramêtres
                    parametres.append(fils.valeur)
        localExpression = racine.expression(parametres)
        #Générer l'expression à partir du tableau des paramêtres
        return localExpression




    def exploration(self, fourmi, idNoeudArbre, arbre, labeldict, graphe, lesChemins, maxFunction):
        if self.isFunction((graphe.nodes[fourmi.noeudCourant]['value'])):
            #Si le noeud Courant de la fourmis n'est pas une fonction alors  =>
            idNoeudCourant =  fourmi.noeudCourant
            noeudCourant =  graphe.nodes[fourmi.noeudCourant]['value']
            #Récupérer le nombre de parametre
            nbParams =  noeudCourant.nbParams
            for j in range(0, nbParams):
                #Récupérer le noeud suivant(voisin) tant que ce n'est pas le noeud précédent
                idSuivant = self.noeudSuivant(idNoeudCourant, graphe)
                while idSuivant == fourmi.noeudPrecedent:
                    idSuivant = self.noeudSuivant(idNoeudCourant, graphe)
                suivant  =   graphe.nodes[idSuivant]['value']
                if(self.isFunction(suivant)):
                    maxFunction = maxFunction -1

                if(maxFunction <= 0):
                    while idSuivant == fourmi.noeudPrecedent or self.isFunction(suivant):
                        idSuivant = self.noeudSuivant(idNoeudCourant, graphe)
                        suivant  =   graphe.nodes[idSuivant]['value']
                
                lesChemins.append((idNoeudCourant, idSuivant))
                #Ajouter le noeud suivant à l'arbre
                arbre.add_node(idNoeudArbre, value=suivant)
                labeldict[idNoeudArbre] = suivant.valeur
                #Liée le nouveau noeud au noeud Pere de l'arbre
                arbre.add_edge(fourmi.noeudArbre, idNoeudArbre)
                #On bascule la fourmi au noeud Suivant
                maFourmi =  Fourmis(idNoeudCourant,idSuivant, idNoeudArbre)
                #On incrémente l'identifiant des noeuds
                idNoeudArbre =  idNoeudArbre + 1
                arbre, lesChemins,  idNoeudArbre, maxFunction = self.exploration(maFourmi, idNoeudArbre, arbre,labeldict,graphe, lesChemins, maxFunction)

        #Ne rien fairepheromone
        return arbre , lesChemins,  idNoeudArbre, maxFunction
    
    def isFunction(self, noeud):
        return hasattr(noeud, 'nbParams')


    def init(self, dataSet, nbIndividu, nbIterration, trigo):
        self.nbIterration = nbIterration
        self.nbIndividu = nbIndividu
        self.dataSet =  dataSet
        self.trigo =  trigo

        variables = sorted(self.dataSet[0].keys())
        print(variables)

        for i in range(0, len(variables)-1):
            self.variablesEntree.append(variables[i])
        self.variablesSortie = variables[len(variables)-1]
        print("Algorithme de colonie de fourmis....")