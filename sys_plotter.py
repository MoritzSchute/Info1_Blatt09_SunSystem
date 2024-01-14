import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np


class SystemPlotter:

    #Klassenvariablen: Plot Sachen
    __fig = plt.figure()
    __ax = plt.axes(projection='3d')


    #Klassendictonary: Farbcode

    __color_dict = {'STA': 'y',
            'OMB': 'navy',
            'TJN': 'chocolate',
            'MCA': 'orchid', 
            'AMO': 'm',
            'CEN': 'c',
            'APO': 'limegreen',
            'ATE': 'royalblue',
            'AST': 'darkorange',
            'IMB': 'teal',
            'MBA': 'fuchsia',
            'PLA': 'b',
            'DWA': 'g',
            'SAT': 'r',
            'TNO': 'springgreen'} 


    def __init__(self, delta_t_print, plot_lim, type_array, specification_array, traces = True):

        #assert...

        self.n_objects = np.shape(type_array)[0]
        self.print_sizes = np.power(1/16 * np.log10(specification_array[:, 0]), 10)
        self.print_colors = [self.__color_dict[type_array[index]] for index in range(self.n_objects)]
        self.delta_t = delta_t_print
        self.lim = plot_lim
        self.traces = traces

        if traces:
            self.place_history = specification_array[:, 1:4]
    
    def plot_SunSystem (self, specifications, time_stamp):

        if self.traces:
            self.place_history = np.append(self.place_history,
                                            specifications[:, 0:3], axis = 0)

        if time_stamp % self.delta_t == 0:
            self.__ax.clear()
            
            self.__ax.set_xlim(-self.lim, self.lim)
            self.__ax.set_ylim(-self.lim, self.lim)
            self.__ax.view_init(-140, 60)

            self.__ax.scatter(specifications[:, 0],
                        specifications[:, 1],
                        specifications[:, 2],
                        s = self.print_sizes,
                        c = self.print_colors)

            if self.traces:

                line_segments = Line3DCollection(
                    self.place_history.reshape(np.shape(self.place_history)[0] // self.n_objects, self.n_objects, 3)
                    .transpose((1,0,2)),
                    lw = self.print_sizes / 30,
                    colors = self.print_colors)

                self.__ax.add_collection(line_segments)
            
            self.__ax.set_title("Day "+ str(int(time_stamp)))
            plt.pause(0.001)





