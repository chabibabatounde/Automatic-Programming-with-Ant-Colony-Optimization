# coding: utf-8
from DataManager import * 
from Visuleur import * 
import os
from algo.eq_Fourmi import *



##########################################################################################################
#Parametrage
##########################################################################################################
typeOptimisation =  "eq"
dataSetFile =  "dataSet/dataset.json"
nbIndividu =  100
nbIterration =  100
trigo =  False

##########################################################################################################
#Initialisations
##########################################################################################################
eq_alogo = [eq_Fourmi()]
coeff_alogo = ["coeff_genetique","coeff_immunitaire"]
solutions = []


##########################################################################################################
#Process
##########################################################################################################

#Chargement des données
dataManager = DataManager(dataSetFile)
visualiseur = Visuleur()
visualiseur.show(dataManager.dataSet)

print("##################################################################################################")
#entree =  raw_input("Voulez vous démarrer le traitement sur ces données ? (O / N)\n")
entree = "o"
os.system('clear')
if entree == "O" or  entree == "o":
    print("Démarrage du processus d'optimisation...")

    if typeOptimisation == "eq":
        print("=> Optimisation d'équation")
        for algorithme in eq_alogo:
            algorithme.init(dataManager.dataSet, nbIndividu, nbIterration, trigo)
            solutions.append(algorithme.run())

    if typeOptimisation == "coeff":
        pass
    
    #print("\nLa solution obtenue est : \n")
    solution =  solutions[0]

    visualiseur.compare(dataManager.dataSet, solution)

