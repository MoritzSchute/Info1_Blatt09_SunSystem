# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:25:15 2024

@author: Moritz Schute
"""

import numpy as np

arr1 = np.array([1,2,3,4,5], dtype = np.int16)
arr2 = np.outer(arr1, np.ones(5))

arr3 = np.stack((arr2, arr2))

arr4 = np.transpose(arr3, axes = (0, 2, 1))
print(arr4-arr3)
print(np.linalg.norm(arr4-arr3, axis = 0))

