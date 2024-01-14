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


TIME_DIF = 86400
DAYS = 2000
system = SunSystem()

t1 = time.time()

for t in range (int(DAYS * 86400 / TIME_DIF)):

	system.move_objects_and_plot(TIME_DIF, TIME_DIF * t / 86400)

t2 = time.time()

print('Zeit für Code: ', t2-t1, end = '   ')