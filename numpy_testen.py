# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:25:15 2024

@author: Moritz Schute
"""

import numpy as np

arr1 = np.array([1,2,3,4,5])
arr_squared = np.outer(arr1, np.ones(len(arr1)))
d = np.diff(arr_squared)
print(arr_squared)
#print(d)
diff = arr_squared - arr_squared.T
print(diff)
