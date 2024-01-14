# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:55:15 2023

@author: Moritz Schute
"""

#from Himmelskoerper_Class import Himmelskoerper
#from test_erde_um_sonne import MiniSunSystem
from SunSystem import SunSystem
#from HugeSunSystem import HugeSunSystem
import matplotlib.pyplot as plt
import numpy as np
import time


#Main

TIME_DIF = 86400
DAYS = 400
system = SunSystem()

t1 = time.time()

system.plot_SunSystem(0)

for t in range (1, int(DAYS * 86400 / TIME_DIF)):

	system.move_objects(TIME_DIF, system.calculate_forces_2_1)

	system.plot_SunSystem_lines(86400 * t / TIME_DIF, 10)

t2 = time.time()

print('Zeit für Code: ', t2-t1, end = '   ')

plt.close()

