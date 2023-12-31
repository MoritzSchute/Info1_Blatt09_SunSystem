# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:34:35 2023

@author: Moritz Schute
"""
import matplotlib.pyplot as plt
import math


class Himmelskoerper:
	"""Klasse für abstrakte Himmelskörper."""
	
	#Klassenvariablen: Plot Sachen
	__fig = plt.figure(figsize= (10,6))
	__ax = plt.axes(projection='3d')
	__ax.set_xlabel('x in m')
	__ax.set_ylabel('y in m')
	__ax.set_zlabel('z in m')
	__ax.set

	#Klassendictonary: Farbcode
	__color_dict = {'STA': 'y', #Stern: gelb
				'PLA': 'b', #Planet: blau
				'DWA': 'g', #Zwergplanet: grün
				'SAT': 'r'} #Satellit: rot
	
	def __init__(self, countable_specifications, type):
		"""
		Weise Instanz Attribute zu (Masse, Position, Startgeschwindigkeit)

		Parameters
		----------
		specifications : numpy array
			Enthält Masse, Position und Startgeschwindigkeit.

		Returns
		-------
		None.

		"""
		#Umrechnungsfaktor, da 
		AE = 1.496*10**11

		self.id = countable_specifications[0]
		self.mass = countable_specifications[1]
		self.pos_x = countable_specifications[2] * AE
		self.pos_y = countable_specifications[3] * AE
		self.pos_z = countable_specifications[4] * AE
		self.vel_x = countable_specifications[5] * AE / 86400
		self.vel_y = countable_specifications[6] * AE / 86400
		self.vel_z = countable_specifications[7] * AE / 86400
		self.type = type
		self.color = self.__color_dict[type]
		self.point_size = math.pow(math.log(self.mass, 10**16), 10)
	
	def plot_Himmelskoerper (self):
		"""Plotte Instanz von Himmelskörper."""

		self.__ax.scatter(self.pos_x, self.pos_y, self.pos_z, s = self.point_size, c = self.color)	

		
	

