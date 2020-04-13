# coding: utf-8
class Soustration:
    def __init__(self):
        self.valeur =  "-"
        self.nbParams =  2

    def expression(self, tab):
        return "("+str(tab[0])+self.valeur+str(tab[1])+")"