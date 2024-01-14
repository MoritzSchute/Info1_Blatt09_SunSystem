import numpy as np


class ForceCalculator1:
    
    def __init__(self, specification_array):

        #assert type(specification_array) == np.ndarray
        #assert np.shape(specification_array)[1] == 4
        #assert np.dtype(specification_array) == np.number

        self.n_objects = np.shape(specification_array)[0]
        self.specifications = specification_array


    def calculate_forces_1(self):

        forces = np.zeros((3, self.n_objects))

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

            forces[0, index1] = sum_x
            forces[1, index1] = sum_y
            forces[2, index1] = sum_z

            return forces







