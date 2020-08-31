# coding: utf-8
class Sin:
    def __init__(self):
        self.valeur =  "sin"
        self.nbParams =  1
    def expression(self, tab):
        return "("+self.valeur+"("+str(tab[0])+")"+")"