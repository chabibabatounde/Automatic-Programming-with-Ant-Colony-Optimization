# coding: utf-8
class Cos:
    def __init__(self):
        self.valeur =  "cos"
        self.nbParams =  1
    def expression(self, tab):
        return "("+self.valeur+"("+str(tab[0])+")"+")"