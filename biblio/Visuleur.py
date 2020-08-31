# coding: utf-8
#import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import *
import networkx as nx

class Visuleur:
    def show(self, dataSet):
        cles  = dataSet[0].keys()
        ###Traitement 2D
        if(len(cles)==2):
            print("Les donnees sont de type 2D")
            x = []
            y = []
            for ligne  in dataSet :
                x.append(ligne[cles[0]])
                y.append(ligne[cles[1]])
            plt.plot(x, y)
            #plt.show()
            plt.clf()


    def drawGraph(self, graphe, labeldict):
        nx.draw(graphe, labels=labeldict, with_labels = True)
        print("\t Graph tracé")
        plt.show()
        plt.clf()

    def compare(self, dataSet, expression):
        cles  = dataSet[0].keys()
        variables = sorted(cles)
        variablesEntree = []
        variablesSortie = ''

        for i in range(0, len(variables)-1):
            variablesEntree.append(variables[i])

        variablesSortie = variables[len(variables)-1]

        ###Traitement 2D
        if(len(cles)==2):
            x = []
            y = []
            yy = []
            for ligne in dataSet:
                littteral =  expression
                for var in variablesEntree:
                    littteral =  littteral.replace(var, str(ligne[var]))
                    x.append(ligne[var])
                    y.append(eval(littteral))
                    yy.append(ligne[variablesSortie])
            plt.plot(x, y)
            plt.plot(x, yy)
            
        plt.show()
        plt.clf()


            