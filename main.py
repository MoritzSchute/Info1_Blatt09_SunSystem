# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:55:15 2023

@author: Moritz Schute
"""

from Himmelskoerper_Class import Himmelskoerper
import matplotlib.pyplot as plt
import numpy as np

# Lade Daten aus CSV-Datei, Überspringe erste Zeile, lasse erstmal Spalten
# 1 und 2 weg, da Name und Typ (Star, Planet,...) erstmal irrelevant.
rohdaten_array = np.genfromtxt("planets_and_moons.csv",
								  delimiter= ",", skip_header=1, 
								  usecols=(0,3,4,5,6,7,8,9))

#Speichere alle Himmelskörper mit List Comprehension in Array
himmelskoerper_array = [Himmelskoerper(rohdaten_array[index]) 
						for index in range (len(rohdaten_array))]

#Plotte alle Himmelskörper erstmal zum Test 
for object in himmelskoerper_array:
	object.plot_Himmelskoerper()
plt.show()