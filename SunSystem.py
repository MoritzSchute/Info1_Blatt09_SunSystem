import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import math
import numpy as np
import time
from force_calculator import ForceCalculator
from sys_plotter import SystemPlotter


class SunSystem:
	"""Klasse für Zustand des Sonnensystems."""
	

	def __init__(self, force_version = 2, lim = 4e11, delta_t_print = 10, traces = True, source = 'planets_and_moons.csv'):
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
		self.specifications = np.genfromtxt(source,
								  delimiter= ",", skip_header=1, 
								  usecols=(0,3,4,5,6,7,8,9))
		self.specifications[:, 2:] *= AE
		self.specifications[:, 5:] /= 86400

		self.types = np.genfromtxt(source, dtype=np.str_,
								  delimiter= ",", skip_header=1, 
								  usecols=2)

		self.n_objects = len(self.types)

		self.forces = np.zeros((3, self.n_objects))

		self.force_calculator = ForceCalculator (force_version)
		self.system_plotter = SystemPlotter (delta_t_print, lim, self.types, self.specifications[:, 1:5], traces)


	def move_objects_and_plot(self, time_increment, time_stamp):

		for index in range(self.n_objects):
			self.specifications[index, 5] = (self.specifications[index, 5] + time_increment / 2 
									* self.forces[0, index] / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + time_increment / 2 
									* self.forces[1, index] / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + time_increment / 2 
									* self.forces[2, index] / self.specifications[index, 1])
		
			self.specifications[index, 2:5] = (self.specifications[index, 2:5] + time_increment 
									* self.specifications[index, 5:8])

		self.forces = self.force_calculator.calculate_forces(self.specifications[:, 1:5])

		self.system_plotter.plot_SunSystem(self.specifications[:, 2:5], time_stamp)

		for index in range(self.n_objects):
			self.specifications[index, 5] = (self.specifications[index, 5] + time_increment / 2 
									* self.forces[0, index] / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + time_increment / 2 
									* self.forces[1, index] / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + time_increment / 2 
									* self.forces[2, index] / self.specifications[index, 1])
