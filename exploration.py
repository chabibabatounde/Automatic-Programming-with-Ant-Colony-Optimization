# coding: utf-8
import random
from Fourmis import *
import pdb
import sys

#Définition des fonctions necessaires à l'algorithm
def evaporation(pheromone):
    return (1 - alpha) * pheromone

def increase(pheromone, fitness):
    return pheromone + (alpha / fitness)

def isFunction(noeud):
    return hasattr(noeud, 'nbParams')

def choisirNoeud(idNoeudCourant, graphe):
    voisins = list(graphe.neighbors(idNoeudCourant))
    position  =  random.randint(0, len(voisins)-1)
    idSuivant = voisins[position]
    return idSuivant

def exploration(fourmi, idNoeudArbre, arbre, labeldict, graphe):
    if isFunction((graphe.nodes[fourmi.noeudCourant]['value'])):
        #Si le noeud Courant de la fourmis n'est pas une fonction alors  =>
        idNoeudCourant =  fourmi.noeudCourant
        noeudCourant =  graphe.nodes[fourmi.noeudCourant]['value']
        #Récupérer le nombre de parametre
        nbParams =  noeudCourant.nbParams
        for j in range(0, nbParams):
            #Récupérer le noeud suivant(voisin) tant que ce n'est pas le noeud précédent
            idSuivant = choisirNoeud(idNoeudCourant, graphe)
            while idSuivant == fourmi.noeudPrecedent:
                idSuivant = choisirNoeud(idNoeudCourant, graphe)
            suivant  =   graphe.nodes[idSuivant]['value']

            #Ajouter le noeud suivant à l'arbre
            arbre.add_node(idNoeudArbre, value=suivant)
            labeldict[idNoeudArbre] = suivant.valeur
            #Liée le nouveau noeud au noeud Pere de l'arbre
            arbre.add_edge(fourmi.noeudArbre, idNoeudArbre)
            #On bascule la fourmi au noeud Suivant
            maFourmi =  Fourmis(idNoeudCourant,idSuivant, idNoeudArbre)
            '''clone.noeudPrecedent = 
            clone.noeudCourant = idSuivant#arbre
            clone.noeudArbre = idNoeudArbre'''
            #On incrémente l'identifiant des noeuds
            idNoeudArbre =  idNoeudArbre + 1
            arbre, idNoeudArbre= exploration(maFourmi, idNoeudArbre, arbre,labeldict,graphe)

    #Si non si le noeud Courant n'est pas une fonction alors  =>
    #Ne rien faire
    return arbre ,  idNoeudArbre

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