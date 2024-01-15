# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:55:15 2023

@author: Moritz Schute
"""
#Imports für Tests und andere Klassen...
#from Himmelskoerper_Class import Himmelskoerper
#from test_erde_um_sonne import MiniSunSystem
#from HugeSunSystem import HugeSunSystem

from SunSystem import SunSystem
import matplotlib.pyplot as plt
import numpy as np
import time

#TIME_DIF beschreibt, in welchen Zeitschritten das System auktualisiert werden soll in Sekunden.
TIME_DIF = 86400
#DAYS beschreibt die Anzahl Tage, die simuliert werden
DAYS = 2000

#erstelle eine Instanz der Klasse SunSystem.
system = SunSystem()

#für Zeitmessung des Programms
t1 = time.time()

for t in range (int(DAYS * 86400 / TIME_DIF)):

	#Aktualisiere und plotte System mit aktuellen Daten
	system.move_objects_and_plot(TIME_DIF, int(TIME_DIF * t / 86400))

t2 = time.time()

print('Zeit für Code: ', t2-t1, end = '   ')