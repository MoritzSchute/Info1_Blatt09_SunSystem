# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:55:15 2023

@author: Moritz Schute
"""

from Himmelskoerper_Class import Himmelskoerper
from test_erde_um_sonne import MiniSunSystem
from SunSystem import SunSystem
import matplotlib.pyplot as plt
import numpy as np
import time


#Main

TIME_DIF = 86400
system = SunSystem()

t1 = time.time()

for t in range (400):

	system.move_objects(TIME_DIF, system.calculate_forces_2)

	system.plot_SunSystem(t)

	#print('Zeit für Plot: ', t4-t3)
	
	if t % 365 == 0:
		pass
		#print(system.specifications[3])

t2 = time.time()
print('Zeit für 400 Tage, Var. 2: ', t2-t1, end = '   ')

"""
t1 = time.time()
for i in range(1000):
	system.calculate_forces_2()
t2 = time.time()
print('Zeit für Kraftberechnung: ', t2-t1, end = '   ')
"""