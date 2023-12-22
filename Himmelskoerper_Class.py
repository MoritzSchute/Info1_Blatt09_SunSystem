# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:34:35 2023

@author: Moritz Schute
"""
import matplotlib.pyplot as plt


class Himmelskoerper:
	"""Klasse für abstrakte Himmelskörper."""
	
	#Klassenvariablen: Plot Sachen
	__fig = plt.figure(figsize= (10,8))
	__ax = plt.axes(projection='3d')
	__ax.set_xlabel('x in AE')
	__ax.set_ylabel('y in AE')
	__ax.set_zlabel('z in AE')
	
	def __init__(self, specifications):
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
		self.__id = specifications[0]
		self.__mass = specifications[1]
		self.pos_x = specifications[2]
		self.pos_y = specifications[3]
		self.pos_z = specifications[4]
		self.vel_x = specifications[5]
		self.vel_y = specifications[6]
		self.vel_z = specifications[7]
	
	def plot_Himmelskoerper (self):
		"""Plotte Instanz von Himmelskörper."""
		self.__ax.scatter(self.pos_x, self.pos_y, self.pos_z)
		