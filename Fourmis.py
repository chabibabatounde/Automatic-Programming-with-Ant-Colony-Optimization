# coding: utf-8
class Fourmis:
    def __init__(self, precedent=None, courant=None, noeudArbre=None):
        #Noeud précédent du graphe (id)
        self.noeudPrecedent =  precedent
        #Noeud courant du graphe (id)
        self.noeudCourant =  courant
        #Noeud arbre (id)
        self.noeudArbre =  noeudArbre