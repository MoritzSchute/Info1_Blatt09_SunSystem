import numpy as np


class ForceCalculator:
    """Klasse für Berechnung der Kräfte unter den Körpern"""

    #Klassenvariable:
    GRAVITATION_CONSTANT = 6.67408e-11
    
    def __init__(self, version):

        """
		Weise Instanz Attribute zu (Version der Kraftberechnung).

		Parameters
		----------
		force_version: int
			Variable für Version der Kräfteberechnung

		Returns
		-------
		None.

		"""

        #assert type(specification_array) == np.ndarray
        #assert np.shape(specification_array)[1] == 4
        #assert np.dtype(specification_array) == np.number

        #Erstelle Klassenvariable
        self.version = version


    def calculate_forces(self, specification_array):

        """
		Berechne alle Kräfte zwischen den Körpern im System.

		Parameters
		----------
		specification_array: np.ndarray
            Array, das x-, y- und z-Positionen aller Körper enthält.

		Returns
		-------
		Array mit gegenseitigen Kräften der Körper aufeinander.

		"""

        if self.version == 1:
            return self.calculate_forces_1(specification_array)
        
        if self.version == 2:
            #Fastest Version!
            return self.calculate_forces_2_1(specification_array)
        
        if self.version == 3:
            return self.calculate_forces_3(specification_array)


    def calculate_forces_1(self, specifications):

        n_objects = np.shape(specifications)[0]
        forces = np.zeros((3, n_objects))

        for index1 in range(n_objects):
            sum_x = 0
            sum_y = 0
            sum_z = 0
            for index2 in range(n_objects):
                if index1 != index2:
                    distanzvektor = np.array([specifications[index2, 1] - specifications[index1, 1],
                                specifications[index2, 2] - specifications[index1, 2],
                                specifications[index2, 3] - specifications[index1, 3]])
                    
                    abstand = np.linalg.norm(distanzvektor)

                    normierter_distanzvektor = distanzvektor / abstand

                    sum_x += (self.GRAVITATION_CONSTANT * specifications[index1, 0] * specifications[index2, 0] 
                                            / abstand**2 * normierter_distanzvektor[0])
                    sum_y += (self.GRAVITATION_CONSTANT * specifications[index1, 0] * specifications[index2, 0]  
                                            / abstand**2 * normierter_distanzvektor[1])
                    sum_z += (self.GRAVITATION_CONSTANT * specifications[index1, 0] * specifications[index2, 0]  
                                            / abstand**2 * normierter_distanzvektor[2])	

            forces[0, index1] = sum_x
            forces[1, index1] = sum_y
            forces[2, index1] = sum_z

        return forces

    def calculate_forces_3(self, specifications):

        n_objects = len(specifications)
        forces = np.zeros((3, n_objects))

        coordinate_array = (np.stack((
                                    np.outer(specifications[:, 1], np.ones(n_objects)),
                                    np.outer(specifications[:, 2], np.ones(n_objects)),
                                    np.outer(specifications[:, 3], np.ones(n_objects))
                                        )))

        coordinate_array -= np.transpose(coordinate_array, axes = (0, 2, 1))

        total_distance_array = np.linalg.norm(coordinate_array, axis = 0) + 0.001


        coordinate_array /= np.stack((total_distance_array, total_distance_array, total_distance_array))

        abs_force_array = np.outer(specifications[:, 0], np.ones(n_objects))
        abs_force_array *= (abs_force_array.T *
                            self.GRAVITATION_CONSTANT / (total_distance_array**2))

        forces[0] = np.sum(coordinate_array[0] * abs_force_array, axis = 0)
        forces[1] = np.sum(coordinate_array[1] * abs_force_array, axis = 0)
        forces[2] = np.sum(coordinate_array[2] * abs_force_array, axis = 0)

        return forces

    def calculate_forces_2_1(self, specifications):

        n_objects = len(specifications)
        forces = np.zeros((3, n_objects))

        x_coordinate_array = np.outer(specifications[:, 1], np.ones(n_objects))
        y_coordinate_array = np.outer(specifications[:, 2], np.ones(n_objects))
        z_coordinate_array = np.outer(specifications[:, 3], np.ones(n_objects))

        x_coordinate_array -= x_coordinate_array.T
        y_coordinate_array -= y_coordinate_array.T
        z_coordinate_array -= z_coordinate_array.T

        squared_distance_array = (x_coordinate_array**2
                            + y_coordinate_array**2 + z_coordinate_array**2) + 0.1

        x_coordinate_array /= np.sqrt(squared_distance_array)
        y_coordinate_array /= np.sqrt(squared_distance_array)
        z_coordinate_array /= np.sqrt(squared_distance_array)

        abs_force_array = np.outer(specifications[:, 0], np.ones(n_objects))
        abs_force_array *= abs_force_array.T
        abs_force_array *= self.GRAVITATION_CONSTANT / squared_distance_array

        forces[0] = np.sum(x_coordinate_array * abs_force_array, axis = 0)
        forces[1] = np.sum(y_coordinate_array * abs_force_array, axis = 0)
        forces[2] = np.sum(z_coordinate_array * abs_force_array, axis = 0)

        return forces




