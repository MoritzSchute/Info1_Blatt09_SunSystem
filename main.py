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
zahl_rohdaten_array = np.genfromtxt("planets_and_moons.csv",
								  delimiter= ",", skip_header=1, 
								  usecols=(0,3,4,5,6,7,8,9))
typ_rohdaten_array = np.genfromtxt("planets_and_moons.csv", dtype=np.str_,
								  delimiter= ",", skip_header=1, 
								  usecols=2)

#Speichere alle Himmelskörper mit List Comprehension in Array
himmelskoerper_array = [Himmelskoerper(zahl_rohdaten_array[index], typ_rohdaten_array[index]) 
						for index in range (len(zahl_rohdaten_array))]

#Plotte alle Himmelskörper erstmal zum Test 
for object in himmelskoerper_array:
	object.plot_Himmelskoerper()
plt.show()

"""

def calculate_res_forces (himmelskoerper_array):
	#Anzahl Körper
	GRAVITATION_CONSTANT = 6.67*10**-11
	l = len(himmelskoerper_array)
	force_array = np.zeros((l, 3))
	for index1, erster_koerper in enumerate(himmelskoerper_array):
		sum_x = 0
		sum_y = 0
		sum_z = 0
		for index2, zweiter_koerper in enumerate(himmelskoerper_array):
			if index1 != index2:
				distanzvektor = np.array([zweiter_koerper.pos_x - erster_koerper.pos_x,
							   zweiter_koerper.pos_y - erster_koerper.pos_y,
							   zweiter_koerper.pos_z - erster_koerper.pos_z])
				abstand = np.sqrt(np.dot(distanzvektor, distanzvektor))
				normierter_distanzvektor = distanzvektor / abstand
				sum_x += (GRAVITATION_CONSTANT * erster_koerper.mass * zweiter_koerper.mass 
										/ abstand**2 * normierter_distanzvektor[0])
				sum_y += (GRAVITATION_CONSTANT * erster_koerper.mass * zweiter_koerper.mass 
										/ abstand**2 * normierter_distanzvektor[1])
				sum_z += (GRAVITATION_CONSTANT * erster_koerper.mass * zweiter_koerper.mass 
										/ abstand**2 * normierter_distanzvektor[2])	
				if(index1 == 0 and index2 == 1):
					print(GRAVITATION_CONSTANT * erster_koerper.mass * zweiter_koerper.mass 
										/ abstand**2)	
		force_array[index1, 0] = sum_x
		force_array[index1, 1] = sum_y
		force_array[index1, 2] = sum_z
						
	return force_array

print(calculate_res_forces(himmelskoerper_array))			

"""
