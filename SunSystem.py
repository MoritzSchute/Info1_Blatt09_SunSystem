import numpy as np
from force_calculator import ForceCalculator
from sys_plotter import SystemPlotter


class SunSystem:
	"""Klasse für Zustand des Sonnensystems."""
	

	def __init__(self, force_version = 2, lim = 4e11, delta_t_print = 10, traces = True, source = 'planets_and_moons.csv'):
		"""
		Weise Instanz Attribute zu (Masse, Position, Startgeschwindigkeit)

		Parameters
		----------
		force_version: int
			Variable für Version der Kräfteberechnung
			Standard: 2, da schnellste version
		lim: int
			Variable für Größe (Ränder) des Plots in m in x- und y-Richtung.
			Standard: 4e11m -> für innere 5 Planeten des Sonnensystems inkl. Monde und einige Satelliten.
		delta_t_print: int
			Zeitabstand zwischen 2 Plots in Tagen
		traces: bool
			True: Bahnverläufe der Körper an
			False: Plot ohne Bahnverläufe
		source: str
			Dateiname der Rohdatendatei
			Standard: kleine Datei mit 178 Körpern

		Returns
		-------
		None.

		"""
		#Umrechnungsfaktor, da Einheiten in AE, bzw. AE/Tag
		AE = 1.496*10**11

		self.GRAVITATION_CONSTANT = 6.67408e-11

        # Lade Daten aus CSV-Datei, Überspringe erste Zeile, lasse erstmal Spalten
        # 1 und 2 weg, da Name und Typ (Star, Planet,...) erstmal irrelevant oder in anderem Array.
		self.specifications = np.genfromtxt(source,
								  delimiter= ",", skip_header=1, 
								  usecols=(0,3,4,5,6,7,8,9))
		
		#Rechne Einheiten in SI-Einheiten um.
		self.specifications[:, 2:] *= AE
		self.specifications[:, 5:] /= 86400

		#Array für Typen der einzelnen Körper (für Farbe der Plots)
		self.types = np.genfromtxt(source, dtype=np.str_,
								  delimiter= ",", skip_header=1, 
								  usecols=2)

		#Variable für Anzahl der Objekte im System
		self.n_objects = len(self.types)

		#Array, in dem wirkende Kräfte der Körper aufeinander gespeichert werden.
		self.forces = np.zeros((3, self.n_objects))

		#Instanz der Klasse Forcecalculator
		self.force_calculator = ForceCalculator (force_version)

		#INstanz der Klasse SystemPlotter
		self.system_plotter = SystemPlotter (delta_t_print, lim, self.types, self.specifications[:, 1:5], traces)


	def move_objects_and_plot(self, time_increment, time_stamp):

		"""
		Aktualisiere Geschwindigkeiten und Positionen und berechne Kräfte neu.

		Parameters
		----------
		time_increment: int
			Variable für Feinheit der Approximation des Bahnverlaufs und 
			Rate der Aktualisierung der Systemparameter.
		time_stamp: int
			Variable für aktuelle Zeit im System.
		
		Returns
		-------
		None.
		"""

		#Aktualisiere für alle Objekte die Geschwindigkeiten und die Position anhand der im vorherigen
		#Durchlauf gemessenen Kräften und berechneten Geschwindigkeiten.
		for index in range(self.n_objects):
			self.specifications[index, 5] = (self.specifications[index, 5] + time_increment / 2 
									* self.forces[0, index] / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + time_increment / 2 
									* self.forces[1, index] / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + time_increment / 2 
									* self.forces[2, index] / self.specifications[index, 1])
		
			self.specifications[index, 2:5] = (self.specifications[index, 2:5] + time_increment 
									* self.specifications[index, 5:8])

		#Berechne Kräfte neu.
		self.forces = self.force_calculator.calculate_forces(self.specifications[:, 1:5])

		#Plotte das System mit den neuen Positionen
		self.system_plotter.plot_SunSystem(self.specifications[:, 2:5], time_stamp)

		#Aktualisiere erneut die Geschwindigkeiten mit den neu berechneten Kräften
		for index in range(self.n_objects):
			self.specifications[index, 5] = (self.specifications[index, 5] + time_increment / 2 
									* self.forces[0, index] / self.specifications[index, 1])
			self.specifications[index, 6] = (self.specifications[index, 6] + time_increment / 2 
									* self.forces[1, index] / self.specifications[index, 1])
			self.specifications[index, 7] = (self.specifications[index, 7] + time_increment / 2 
									* self.forces[2, index] / self.specifications[index, 1])
