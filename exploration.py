# coding: utf-8
import random
from operator import itemgetter
from Fourmis import *
from math import *
import networkx as nx
import sys

learningRate = 0.95


def miseAJour(graphe, lesChemins, fitness, alpha):
    # Renforcement
    for lignes in lesChemins:
        graphe[lignes[0]][lignes[1]]['pheromone'] = (graphe[lignes[0]][lignes[1]]['pheromone']) + (alpha /fitness)
    # Evaporation
    for lignes in graphe.edges():
        graphe[lignes[0]][lignes[1]]['pheromone'] = (1 - alpha) * graphe[lignes[0]][lignes[1]]['pheromone']

    return graphe

def rawFitness(dataSet, expression,  parametre):
    fitness =  0
    for ligne in dataSet:
        local = eval(expression.replace(parametre,str(ligne['in'])))
        fitness = fitness + abs(ligne['out'] - local)
        #print("\t"+str(expression.replace(parametre,str(ligne['in'])))+" = " +str(abs(ligne['out'] - local)))
    fitness =  fitness / len(dataSet)
    return fitness

def noeudSuivant(idNoeud, graphe):
    qZero = random.uniform(0, 1)
    idSuivant =  idNoeud
    if(qZero > learningRate):
        #Choix aléatoire
        voisins = list(graphe.neighbors(idNoeud))
        position  =  random.randint(0, len(voisins)-1)
        idSuivant = voisins[position]
    else:
        voisins = list(graphe.neighbors(idNoeud))
        total = 0
        roulette =  []
        for suivant in voisins:
            total = total + graphe[idNoeud][suivant]['pheromone']
        estqi =  0
        for suivant in voisins:
            proba = round(graphe[idNoeud][suivant]['pheromone'] * 100 / total)
            estqi = estqi + proba
            for j in range(0, int(proba)):
                roulette.append(suivant)
        choix = random.randint(0, len(roulette)-1)
        idSuivant = roulette[choix]
    return idSuivant

def exploration(fourmi, idNoeudArbre, arbre, labeldict, graphe, lesChemins, maxFunction):
    if isFunction((graphe.nodes[fourmi.noeudCourant]['value'])):
        #Si le noeud Courant de la fourmis n'est pas une fonction alors  =>
        idNoeudCourant =  fourmi.noeudCourant
        noeudCourant =  graphe.nodes[fourmi.noeudCourant]['value']
        #Récupérer le nombre de parametre
        nbParams =  noeudCourant.nbParams
        for j in range(0, nbParams):
            #Récupérer le noeud suivant(voisin) tant que ce n'est pas le noeud précédent
            idSuivant = noeudSuivant(idNoeudCourant, graphe)
            while idSuivant == fourmi.noeudPrecedent:
                idSuivant = noeudSuivant(idNoeudCourant, graphe)
            suivant  =   graphe.nodes[idSuivant]['value']
            if(isFunction(suivant)):
                maxFunction = maxFunction -1

            if(maxFunction <= 0):
                while idSuivant == fourmi.noeudPrecedent or isFunction(suivant):
                    idSuivant = noeudSuivant(idNoeudCourant, graphe)
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
            arbre, lesChemins,  idNoeudArbre, maxFunction = exploration(maFourmi, idNoeudArbre, arbre,labeldict,graphe, lesChemins, maxFunction)

    #Ne rien faire
    return arbre , lesChemins,  idNoeudArbre, maxFunction


#Définition des fonctions necessaires à l'algorithm
def isFunction(noeud):
    return hasattr(noeud, 'nbParams')

def choisirNoeud(idNoeudCourant, graphe):
    voisins = list(graphe.neighbors(idNoeudCourant))
    position  =  random.randint(0, len(voisins)-1)
    idSuivant = voisins[position]
    return idSuivant



def choisirChemin(idNoeudCourant, precedent, graphe):
    voisins = list(graphe.neighbors(idNoeudCourant))
    maxi = 0
    old = 0
    for nd in voisins:
        pheromone = graphe[idNoeudCourant][nd]
        if (pheromone > old and nd != precedent):
            old = pheromone
            maxi = nd
    return maxi


def meilleursNoeud(idNoeudCourant, precedent, graphe, limite):
    voisins = list(graphe.neighbors(idNoeudCourant))
    lesNoeud = []
    for nd in voisins:
        pheromone = graphe[idNoeudCourant][nd]
        if (nd != precedent):
            lesNoeud.append({"pheromone" : pheromone['pheromone'], "idNoeud" :  nd, })
    
    lesNoeud =  sorted(lesNoeud, key=itemgetter('pheromone'), reverse=True)
    return lesNoeud[:limite]


def construire(graphe, grapheNodes, noeudDemarrage):
    labeldict = {}
    arbre = nx.Graph()
    idNoeudArbre = 0
    noeudCourant = grapheNodes[noeudDemarrage]
    arbre.add_node(idNoeudArbre, value=noeudCourant)
    labeldict[idNoeudArbre] = noeudCourant.valeur
    fourmi = Fourmis(noeudDemarrage, noeudDemarrage,  idNoeudArbre)
    idNoeudArbre =  idNoeudArbre + 1
    lesChemins = []
    arbre , lesChemins,  idNoeudArbre = explorationConstrction(fourmi, idNoeudArbre, arbre, labeldict, graphe, lesChemins)
    nx.draw(arbre, labels=labeldict, with_labels = True)
    expressionLitterale = parcourir(0, arbre)
    return expressionLitterale, arbre


def explorationConstrction(fourmi, idNoeudArbre, arbre, labeldict, graphe, lesChemins):
    if isFunction((graphe.nodes[fourmi.noeudCourant]['value'])):
        #Si le noeud Courant de la fourmis n'est pas une fonction alors  =>
        idNoeudCourant =  fourmi.noeudCourant
        noeudCourant =  graphe.nodes[fourmi.noeudCourant]['value']
        #Récupérer le nombre de parametre
        nbParams =  noeudCourant.nbParams
        suivants = meilleursNoeud(idNoeudCourant, fourmi.noeudPrecedent, graphe ,nbParams)
        for noeud in suivants:
            idSuivant =  noeud['idNoeud']
            suivant  =   graphe.nodes[idSuivant]['value']
            #Ajouter le noeud suivant à l'arbre
            arbre.add_node(idNoeudArbre, value=suivant)
            labeldict[idNoeudArbre] = suivant.valeur
            #Liée le nouveau noeud au noeud Pere de l'arbre
            arbre.add_edge(fourmi.noeudArbre, idNoeudArbre)
            #On bascule la fourmi au noeud Suivant
            maFourmi =  Fourmis(idNoeudCourant,idSuivant, idNoeudArbre)
            #On incrémente l'identifiant des noeuds
            idNoeudArbre =  idNoeudArbre + 1
            arbre, lesChemins,  idNoeudArbre = exploration(maFourmi, idNoeudArbre, arbre,labeldict,graphe, lesChemins)
    return arbre , lesChemins,  idNoeudArbre


def parcourir(idNoeud, arbre, ancetre=None):
    #sys.setrecursionlimit(10)
    #Récupérer le noeud racine
    racine = arbre.nodes[idNoeud]['value']
    #Initialiser "Expression" à ""
    localExpression = ""
    #Initialiser le tableau des paramêtres à vide
    parametres = []
    #Si c'est une fonction
    if(isFunction(racine)):
        #Récupérer les fils
        listDesFils =  list(arbre.neighbors(idNoeud))
        #Pour chaque fils :
        for i in listDesFils:
            #récupérer la valeur
            fils = arbre.nodes[i]['value']
            #Si le noeud est une fonction :
            if isFunction(fils):
                #On vérifie si on ne va pas en arriere
                if(i != ancetre):
                    sortie = parcourir(i, arbre, idNoeud)
                    #Ajouter l'expression dans le tableau des paramêtres
                    parametres.append(sortie)
            #Si le noeud est un terminal
            else :
                #Ajouter la valeur"dans le tableau des paramêtres
                parametres.append(fils.valeur)
    localExpression = racine.expression(parametres)
    #Générer l'expression à partir du tableau des paramêtres
    return localExpression

def decrire(graphe):
    for ed in graphe.edges():
        print(ed, graphe[ed[0]][ed[1]])



def adjustedFitness(fitness):
    alpha = 1 / (1 + fitness)
    return alpha