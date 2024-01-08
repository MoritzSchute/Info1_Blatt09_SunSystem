# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:55:15 2023

@author: Moritz Schute
"""

from Himmelskoerper_Class import Himmelskoerper
import matplotlib.pyplot as plt
import numpy as np


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
	
		force_array[index1, 0] = sum_x
		force_array[index1, 1] = sum_y
		force_array[index1, 2] = sum_z
						
	return force_array

def move_object(object, forces, time_increment):
	object.vel_x = object.vel_x + time_increment / 2 * forces[0] / object.mass
	object.vel_y = object.vel_y + time_increment / 2 * forces[1] / object.mass
	object.vel_z = object.vel_z + time_increment / 2 * forces[2] / object.mass
	
	object.pos_x = object.pos_x + time_increment * object.vel_x
	object.pos_y = object.pos_y + time_increment * object.vel_y
	object.pos_z = object.pos_z + time_increment * object.vel_z


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

#Main
TIME_DIF = 86400
t = 0
for t in range (365):
	forces = calculate_res_forces(himmelskoerper_array)
	Himmelskoerper.ax.clear()
	for index, object in enumerate(himmelskoerper_array):
		move_object(object, forces[index], TIME_DIF)
		object.plot_Himmelskoerper()
	Himmelskoerper.ax.set_title("Day "+ str(t))
	print(t)
	plt.draw()
	plt.pause(0.01)
	