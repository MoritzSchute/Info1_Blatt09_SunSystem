import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import math
import numpy as np
import time
from force_calculator import ForceCalculator


class SunSystem:
	"""Klasse für Zustand des Sonnensystems."""
	
	#plt.ioff()
	#Klassenvariablen: Plot Sachen
	__fig = plt.figure()
	__ax = plt.axes(projection='3d')


	#Klassendictonary: Farbcode
	__color_dict = {'STA': 'y', #Stern: gelb
				'PLA': 'b', #Planet: blau
				'DWA': 'g', #Zwergplanet: grün
				'SAT': 'r'} #Satellit: rot
	
	
	def __init__(self, force_version):
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
		#Umrechnungsfaktor, da Einheiten in AE, bzw. AE/Tag
		AE = 1.496*10**11
		self.GRAVITATION_CONSTANT = 6.67408e-11

        # Lade Daten aus CSV-Datei, Überspringe erste Zeile, lasse erstmal Spalten
        # 1 und 2 weg, da Name und Typ (Star, Planet,...) erstmal irrelevant.
		self.specifications = np.genfromtxt("planets_and_moons.csv",
								  delimiter= ",", skip_header=1, 
								  usecols=(0,3,4,5,6,7,8,9))
		self.specifications[:, 2:] *= AE
		self.specifications[:, 5:] /= 86400

		self.types = np.genfromtxt("planets_and_moons.csv", dtype=np.str_,
								  delimiter= ",", skip_header=1, 
								  usecols=2)
		self.n_objects = len(self.types)
		self.print_sizes = np.power(1/16 * np.log10(self.specifications[:, 1]), 10)
		self.print_colors = [self.__color_dict[self.types[index]] for index in range(self.n_objects)]

		self.forces = np.zeros((3, self.n_objects))

		self.place_history = self.specifications[:, 2:5]

		self.force_version = force_version




	def plot_SunSystem (self, time_stamp):
		"""Plotte Sonnensystem skaliert."""
		if time_stamp % 10 == 0:
			self.__ax.clear()
			
			lim = 4e11
			self.__ax.set_xlim(-lim, lim)
			self.__ax.set_ylim(-lim, lim)
			self.__ax.view_init(-140, 60)
			
			self.__ax.scatter(self.specifications[:, 2],
						self.specifications[:, 3],
						self.specifications[:, 4],
						s = self.print_sizes,
						c = self.print_colors)

			self.__ax.set_title("Day"+ str(time_stamp))
			plt.pause(0.01)
	

	def plot_SunSystem_lines (self, time_stamp, delta_t_print):
		"""Plotte Sonnensystem skaliert."""
		self.place_history = np.append(self.place_history, self.specifications[:, 2:5], axis = 0)
		if time_stamp % delta_t_print == 0:
			self.__ax.clear()

			lim = 4e11
			self.__ax.set_xlim(-lim, lim)
			self.__ax.set_ylim(-lim, lim)
			self.__ax.view_init(-140, 60)

			self.__ax.scatter(self.specifications[:, 2],
						self.specifications[:, 3],
						self.specifications[:, 4],
						s = self.print_sizes,
						c = self.print_colors)

			line_segments = Line3DCollection(
				self.place_history.reshape(np.shape(self.place_history)[0] // self.n_objects, self.n_objects, 3)
				.transpose((1,0,2)),
				lw = 1,
				colors = self.print_colors)

			self.__ax.add_collection(line_segments)

			self.__ax.set_title("Day "+ str(int(time_stamp)))
			plt.pause(0.1)



	def move_objects(self, time_increment):
		for index in range(self.n_objects):
			self.specifications[index, 5] = (self.specifications[index, 5] + time_increment / 2 
									* self.forces[0, index] / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + time_increment / 2 
									* self.forces[1, index] / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + time_increment / 2 
									* self.forces[2, index] / self.specifications[index, 1])
			self.specifications[index, 2] = (self.specifications[index, 2] + time_increment 
									* self.specifications[index, 5])
			self.specifications[index, 3] = (self.specifications[index, 3] + time_increment 
									* self.specifications[index, 6])
			self.specifications[index, 4] = (self.specifications[index, 4] + time_increment 
									* self.specifications[index, 7])

		force_calculator = ForceCalculator(self.specifications[:, 1:5], 2)
		self.forces = force_calculator.calculate_forces()
		#print(self.forces)

		for index in range(self.n_objects):

			self.specifications[index, 5] = (self.specifications[index, 5] + time_increment / 2 
									* self.forces[0, index] / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + time_increment / 2 
									* self.forces[1, index] / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + time_increment / 2 
									* self.forces[2, index] / self.specifications[index, 1])


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

					sum_x += (self.GRAVITATION_CONSTANT * self.specifications[index1, 1] * self.specifications[index2, 1] 
											/ abstand**2 * normierter_distanzvektor[0])
					sum_y += (self.GRAVITATION_CONSTANT * self.specifications[index1, 1] * self.specifications[index2, 1]  
											/ abstand**2 * normierter_distanzvektor[1])
					sum_z += (self.GRAVITATION_CONSTANT * self.specifications[index1, 1] * self.specifications[index2, 1]  
											/ abstand**2 * normierter_distanzvektor[2])	

			self.forces[0, index1] = sum_x
			self.forces[1, index1] = sum_y
			self.forces[2, index1] = sum_z

	def calculate_forces_2(self):
		mass_array = self.specifications[:, 1]

		x_coordinate_array = np.outer(self.specifications[:, 2], np.ones(self.n_objects))
		y_coordinate_array = np.outer(self.specifications[:, 3], np.ones(self.n_objects))
		z_coordinate_array = np.outer(self.specifications[:, 4], np.ones(self.n_objects))

		x_distance_array = x_coordinate_array - x_coordinate_array.T
		y_distance_array = y_coordinate_array - y_coordinate_array.T
		z_distance_array = z_coordinate_array - z_coordinate_array.T

		squared_distance_array = (x_distance_array**2
						   + y_distance_array**2 + z_distance_array**2) + 0.1

		norm_x_distance_array = x_distance_array / np.sqrt(squared_distance_array)
		norm_y_distance_array = y_distance_array / np.sqrt(squared_distance_array)
		norm_z_distance_array = z_distance_array / np.sqrt(squared_distance_array)

		abs_force_array = np.outer(mass_array, np.ones(self.n_objects))
		abs_force_array *= abs_force_array.T
		abs_force_array *= self.GRAVITATION_CONSTANT / squared_distance_array

		self.forces[0] = np.sum(norm_x_distance_array * abs_force_array, axis = 0)
		self.forces[1] = np.sum(norm_y_distance_array * abs_force_array, axis = 0)
		self.forces[2] = np.sum(norm_z_distance_array * abs_force_array, axis = 0)

	def calculate_forces_3_test(self):
		#mass_array = self.specifications[:, 1]
		
		t1 = time.time()
		for i in range(10000):
			coordinate_array = (np.stack((
										np.outer(self.specifications[:, 2], np.ones(self.n_objects)),
										np.outer(self.specifications[:, 3], np.ones(self.n_objects)),
										np.outer(self.specifications[:, 4], np.ones(self.n_objects))
										   )))
		t2 = time.time()
		print('Zeit für Outer Prod: ', t2-t1)
		
		
		
		t1 = time.time()
		for i in range(10000):
			coordinate_array -= np.transpose(coordinate_array, axes = (0, 2, 1))
		t2 = time.time()
		print('Zeit für Diff: ', t2-t1)
		
		
		t1 = time.time()
		for i in range(10000):
			total_distance_array = np.linalg.norm(coordinate_array, axis = 0) + 0.001
		t2 = time.time()
		print('Zeit für distance**2: ', t2-t1)
		print(id(coordinate_array))
		
		
		
		t1 = time.time()
		for i in range(10000):
			for j in range(3):
				coordinate_array[j] /= total_distance_array
		t2 = time.time()
		print('Zeit für norm distance: ', t2-t1)
		
		
		
		
		t1 = time.time()
		for i in range(10000):
			abs_force_array = np.outer(self.specifications[:, 1], np.ones(self.n_objects))
			abs_force_array *= (abs_force_array.T *
							   self.GRAVITATION_CONSTANT / (total_distance_array**2))
		t2 = time.time()
		print('Zeit für abs force: ', t2-t1)
		
		
		
		t1 = time.time()
		for i in range(10000):
			self.forces[0] = np.sum(coordinate_array[0] * abs_force_array, axis = 0)
			self.forces[1] = np.sum(coordinate_array[1] * abs_force_array, axis = 0)
			self.forces[2] = np.sum(coordinate_array[2] * abs_force_array, axis = 0)
		t2 = time.time()
		print('Zeit für force update: ', t2-t1)
		
	def calculate_forces_3(self):

		coordinate_array = (np.stack((
									np.outer(self.specifications[:, 2], np.ones(self.n_objects)),
									np.outer(self.specifications[:, 3], np.ones(self.n_objects)),
									np.outer(self.specifications[:, 4], np.ones(self.n_objects))
									   )))

		coordinate_array -= np.transpose(coordinate_array, axes = (0, 2, 1))

		total_distance_array = np.linalg.norm(coordinate_array, axis = 0) + 0.001


		coordinate_array /= np.stack((total_distance_array, total_distance_array, total_distance_array))

		abs_force_array = np.outer(self.specifications[:, 1], np.ones(self.n_objects))
		abs_force_array *= (abs_force_array.T *
						   self.GRAVITATION_CONSTANT / (total_distance_array**2))

		self.forces[0] = np.sum(coordinate_array[0] * abs_force_array, axis = 0)
		self.forces[1] = np.sum(coordinate_array[1] * abs_force_array, axis = 0)
		self.forces[2] = np.sum(coordinate_array[2] * abs_force_array, axis = 0)

	def calculate_forces_2_1(self):

		x_coordinate_array = np.outer(self.specifications[:, 2], np.ones(self.n_objects))
		y_coordinate_array = np.outer(self.specifications[:, 3], np.ones(self.n_objects))
		z_coordinate_array = np.outer(self.specifications[:, 4], np.ones(self.n_objects))

		x_coordinate_array -= x_coordinate_array.T
		y_coordinate_array -= y_coordinate_array.T
		z_coordinate_array -= z_coordinate_array.T

		squared_distance_array = (x_coordinate_array**2
						   + y_coordinate_array**2 + z_coordinate_array**2) + 0.1

		x_coordinate_array /= np.sqrt(squared_distance_array)
		y_coordinate_array /= np.sqrt(squared_distance_array)
		z_coordinate_array /= np.sqrt(squared_distance_array)

		abs_force_array = np.outer(self.specifications[:, 1], np.ones(self.n_objects))
		abs_force_array *= abs_force_array.T
		abs_force_array *= self.GRAVITATION_CONSTANT / squared_distance_array

		self.forces[0] = np.sum(x_coordinate_array * abs_force_array, axis = 0)
		self.forces[1] = np.sum(y_coordinate_array * abs_force_array, axis = 0)
		self.forces[2] = np.sum(z_coordinate_array * abs_force_array, axis = 0)
