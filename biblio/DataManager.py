# coding: utf-8
import json

class DataManager:
    dataSetString = "[]"
    dataSet = []
    fichier = ""

    def __init__(self, fichier):
        with open(fichier, 'r') as f:
            self.dataSetString = f
            self.dataSet = json.load(f)
        print "Donnees lues avec succes"