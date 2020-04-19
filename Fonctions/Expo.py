
# coding: utf-8
class Expo:
    def __init__(self):
        self.valeur =  "exp"
        self.nbParams =  1
    def expression(self, tab):
        return "("+self.valeur+"("+str(tab[0])+")"+")"