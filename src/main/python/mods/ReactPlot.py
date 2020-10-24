import matplotlib.pyplot as plt


class PlotStuff:
    def __init__(self, g_data):

        self.plot_scf_done(g_data["SCF Done"])

    def plot_scf_done(self, energies):
        """

        :param energies:
        :return:
        """
        plt.plot(energies)
        plt.ylabel('Energy (a.u.)')
        plt.show()

