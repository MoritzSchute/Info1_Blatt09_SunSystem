import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np


class SystemPlotter:

    #Figur und 3D Koordinatensystem für Plot
    __fig = plt.figure()
    __ax = plt.axes(projection='3d')

    #Klassendictonary: Farbcode für Plot

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

        """
        Weise Instanz Attribute zu (Zeitabstand zwischen Plot, Plotgrenzen, ...).

        Parameters
        ----------
        delta_t_print: int
            Zeitabstand zwischen 2 Plots in Tagen.
        plot_lim: int
            Variable für Größe (Ränder) des Plots in m in x- und y-Richtung.
        type_array: np.ndarray
            Array, das Typen der einzelnen Körper enthält.
        specification_array: np.ndarray
            Array, das Massen und x-, y-, und z-Koordinaten der Startpositionen enthält.
        traces: bool
            True: Bahnverläufe der Körper an
            False: Plot ohne Bahnverläufe

        Returns
        -------
        None.

        """

        #assert...

        #Anzahl Objekte im System.
        self.n_objects = np.shape(type_array)[0]

        #Definiere Größen der Scatterpunkte über Masse der Körper
        self.print_sizes = np.power(1/16 * np.log10(specification_array[:, 0]), 10)

        #Weise dem Array die Farben für den Plot anhand des Typs zu.
        self.print_colors = [self.__color_dict[type_array[index]] for index in range(self.n_objects)]

        #Speichere Parameter in Klassenvariablen 
        self.delta_t = delta_t_print
        self.lim = plot_lim
        self.traces = traces

        #Falls Bahnverläufe gefordert sind: Erstelle Array mit Historie der Positionen
        if traces:
            self.place_history = specification_array[:, 1:4]
    
    def plot_SunSystem (self, specifications, time_stamp):

        """
        Plotte aktuellen Zustand des Systems

        Parameters
        ----------
        specifications: np.ndarray
            Array, das x-, y-, und z-Koordinaten der Körper enthält.
        time_stamp: int
            aktuelle Zeit im System für Titel des Plots

        Returns
        -------
        None.

        """

        #Speichere nach jeder Neuberechnung Positionen ab, für Bahnverläufe, falls gefordert.
        if self.traces:
            self.place_history = np.append(self.place_history,
                                            specifications[:, 0:3], axis = 0)

        #Im geforderten Abstand plotte das System:
        if time_stamp % self.delta_t == 0:

            #Lösche alten Plot
            self.__ax.clear()
            
            #Passe Ränder und Blickwinkel an
            self.__ax.set_xlim(-self.lim, self.lim)
            self.__ax.set_ylim(-self.lim, self.lim)
            self.__ax.view_init(-140, 60)

            #Plotte Körper mit entsprechender Größe und Farbe
            self.__ax.scatter(specifications[:, 0],
                        specifications[:, 1],
                        specifications[:, 2],
                        s = self.print_sizes,
                        c = self.print_colors)

            #Plotte Bahnlinien falls gefordert
            if self.traces:

                #line_segments enthält alle Linien in 3DCollection aus place_history-Array mit
                #entsprechenden Linienbreiten und Linienfarben
                line_segments = Line3DCollection(
                    self.place_history.reshape(np.shape(self.place_history)[0] // self.n_objects, self.n_objects, 3)
                    .transpose((1,0,2)),
                    lw = self.print_sizes / 30,
                    colors = self.print_colors)

                #Füge die ganzen Bahnlinien dem Plot hinzu
                self.__ax.add_collection(line_segments)
            
            #Setze Titel je nach Zeit im System
            self.__ax.set_title("Day "+ str(int(time_stamp)))

            #Plotte und sleep 0.001s
            plt.pause(0.001)





