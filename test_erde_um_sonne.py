import matplotlib.pyplot as plt
import math
import numpy as np
from numpy import linalg
import time


class MiniSunSystem:
	"""Klasse für Zustand des Sonnensystems."""
	
	#Klassenvariablen: Plot Sachen
	__fig = plt.figure(figsize= (10,6))
	__ax = plt.axes(projection='3d')



	#Klassendictonary: Farbcode
	__color_dict = {'STA': 'y', #Stern: gelb
				'PLA': 'b', #Planet: blau
				'DWA': 'g', #Zwergplanet: grün
				'SAT': 'r'} #Satellit: rot
	
	def __init__(self):
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
		self.SUN_MASS = 1.989e30
		self.EARTH_MASS = 5.9722e24
		self.EARTH_RADIUS = 150000000000
		self.GRAVITATION_CONSTANT = 6.67408e-11
		EARTH_VEL_0 = -math.sqrt(self.GRAVITATION_CONSTANT * self.SUN_MASS / self.EARTH_RADIUS)

		self.specifications = np.array([[0, self.SUN_MASS, 0,0,0,0,0,0],
								   [1, self.EARTH_MASS, self.EARTH_RADIUS, 0, 0, 0, EARTH_VEL_0, 0]])
		self.types = np.array(['STA', 'PLA'], dtype=np.str_)
		self.n_objects = len(self.types)
		self.print_sizes = np.power(1/16 * np.log10(self.specifications[:, 1]), 10)
		self.print_colors = [self.__color_dict[self.types[index]] for index in range(self.n_objects)]

		self.forces = np.zeros((self.n_objects, 3))



	def plot_SunSystem (self, time_stamp):
		"""Plotte Sonnensystem skaliert."""
		lim = 2e11

		if time_stamp % 10 == 0:
			#self.__ax.clear()
			self.__ax.set_xlim(-lim, lim)
			self.__ax.set_ylim(-lim, lim)
			self.__ax.view_init(-140, 60)
			for index in range (self.n_objects):
				self.__ax.scatter(self.specifications[index, 2],
						self.specifications[index, 3],
						self.specifications[index, 4],
						s = self.print_sizes[index],
						c = self.print_colors[index])

			self.__ax.set_title("Day"+ str(time_stamp))
			plt.pause(0.01)


	def calculate_forces_1(self):
		
		for index1 in range(self.n_objects):
			sum_x = 0
			sum_y = 0
			sum_z = 0
			for index2 in range(self.n_objects):
				if index1 != index2:
					distanzvektor = np.array([self.specifications[index2, 2] - self.specifications[index1, 2],
								self.specifications[index2, 3] - self.specifications[index1, 3],
								self.specifications[index2, 4] - self.specifications[index1, 4]])
					
					abstand = np.linalg.norm(distanzvektor)

					normierter_distanzvektor = distanzvektor / abstand
					sum_x += (self.GRAVITATION_CONSTANT * self.EARTH_MASS * self.SUN_MASS 
											 * normierter_distanzvektor[0] / (abstand ** 2))
					sum_y += (self.GRAVITATION_CONSTANT * self.EARTH_MASS * self.SUN_MASS 
											 * normierter_distanzvektor[1] / (abstand ** 2))
					sum_z += (self.GRAVITATION_CONSTANT * self.EARTH_MASS * self.SUN_MASS 
											 * normierter_distanzvektor[2] / (abstand ** 2))

			self.forces[index1, 0] = sum_x 
			self.forces[index1, 1] = sum_y 
			self.forces[index1, 2] = sum_z



	def move_objects(self, time_increment, force_func):
		for index in range(self.n_objects):
			self.specifications[index, 5] = (self.specifications[index, 5] + ((time_increment / 2) 
									* self.forces[index, 0]) / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + ((time_increment / 2) 
									* self.forces[index, 1]) / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + ((time_increment / 2) 
									* self.forces[index, 2]) / self.specifications[index, 1])
			self.specifications[index, 2] = (self.specifications[index, 2] + time_increment 
									* self.specifications[index, 5])
			self.specifications[index, 3] = (self.specifications[index, 3] + time_increment 
									* self.specifications[index, 6])
			self.specifications[index, 4] = (self.specifications[index, 4] + time_increment 
									* self.specifications[index, 7])


		force_func()
		

		for index in range(self.n_objects):

			self.specifications[index, 5] = (self.specifications[index, 5] + ((time_increment / 2) 
									* self.forces[index, 0]) / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + ((time_increment / 2) 
									* self.forces[index, 1]) / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + ((time_increment / 2) 
									* self.forces[index, 2]) / self.specifications[index, 1])

	def calculate_forces_2(self):
		mass_array = self.specifications[:, 1]
		
		x_coordinate_array = np.outer(self.specifications[:, 2], np.ones(self.n_objects))
		y_coordinate_array = np.outer(self.specifications[:, 3], np.ones(self.n_objects))
		z_coordinate_array = np.outer(self.specifications[:, 4], np.ones(self.n_objects))

		#print(x_coordinate_array, y_coordinate_array, z_coordinate_array)

		x_distance_array = x_coordinate_array - x_coordinate_array.T
		y_distance_array = y_coordinate_array - y_coordinate_array.T
		z_distance_array = z_coordinate_array - z_coordinate_array.T
		
		#print(x_distance_array, y_distance_array, z_distance_array)

		squared_distance_array = (x_distance_array**2
						   + y_distance_array**2 + z_distance_array**2) + 0.1

		norm_x_distance_array = x_distance_array / np.sqrt(squared_distance_array)
		norm_y_distance_array = y_distance_array / np.sqrt(squared_distance_array)
		norm_z_distance_array = z_distance_array / np.sqrt(squared_distance_array)

		abs_force_array = np.outer(mass_array, np.ones(self.n_objects))
		#print(abs_force_array)
		abs_force_array *= abs_force_array.T
		#print(abs_force_array)
		abs_force_array *= self.GRAVITATION_CONSTANT / squared_distance_array
		#print(abs_force_array)
		
		#print(norm_x_distance_array * abs_force_array)

		self.forces[:, 0] = np.sum(norm_x_distance_array * abs_force_array, axis = 0)
		self.forces[:, 1] = np.sum(norm_y_distance_array * abs_force_array, axis = 0)
		self.forces[:, 2] = np.sum(norm_z_distance_array * abs_force_array, axis = 0)

		#print(self.forces)
