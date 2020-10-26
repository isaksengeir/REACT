import matplotlib.pyplot as plt
import matplotlib as mpl


class PlotStuff:
    def __init__(self, g_data, filename):

        self.g_data = g_data
        self.filename = filename

        self.set_plot_settings()

    def set_plot_settings(self):
        """
        Defines mpl.rcParams
        :return:
        """
        #REACT color scheme:
        react_white = "#dcdcdc"
        react_blue = "#6272a4"
        react_pink = "#8f1777"
        react_bg_dark = "#141414"
        react_bg = "#1e1e1e"
        #General settings
        mpl.rcParams["xtick.color"] = react_white
        mpl.rcParams["ytick.color"] = react_white

        #Main figure frame
        mpl.rcParams["figure.facecolor"] = react_bg_dark
        mpl.rcParams["figure.edgecolor"] = react_blue

        mpl.rcParams["figure.autolayout"] = True

        #TODO this or tight_layout (overrides these settings)
        mpl.rcParams["figure.subplot.top"] = 0.88
        mpl.rcParams["figure.subplot.wspace"] = 0.70
        mpl.rcParams["figure.subplot.hspace"] = 0.35
        mpl.rcParams["figure.subplot.right"] = 0.96

        #Subplots
        mpl.rcParams["axes.facecolor"] = react_bg
        mpl.rcParams["axes.titlecolor"] = react_pink
        mpl.rcParams["axes.edgecolor"] = react_blue
        #mpl.rcParams["axes.labelcolor"] = react_pink
        mpl.rcParams["text.color"] = react_blue
        mpl.rcParams["axes.titleweight"] = "bold"
        mpl.rcParams["axes.formatter.useoffset"] = "False"

        #TODO:
        # savefig.format:    png         # {png, ps, pdf, svg}

        mpl.rcParams["axes.prop_cycle"] = mpl.cycler('color', ['8f1777', '1f77b4', 'ff7f0e', '2ca02c', 'd62728',
                                                       '9467bd', '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf'])

    def plot_scf_done(self):
        """
        Creates single plot with SCF Done energies
        :param energies:
        :return:
        """
        plt.plot(self.g_data["SCF Done"])
        plt.ylabel('Energy (a.u.)')
        plt.xlabel('Iteration')

        plt.show()

    def plot_convergence(self):
        """
        plot Force and displacement (max and rms)
        :return:
        """
        # Set up the figure
        fig, axs = plt.subplots(nrows=2, ncols=2)
        axs = axs.flatten()
        fig.tight_layout()

        axs[0].set_title('Maximum Force')
        axs[1].set_title('RMS Force')
        axs[2].set_title('Maximum displacement')
        axs[3].set_title('RMS displacement')

        axs[0].plot(self.g_data["Maximum Force"])
        axs[1].plot(self.g_data["RMS     Force"])
        axs[2].plot(self.g_data["Maximum Displacement"])
        axs[3].plot(self.g_data["RMS     Displacement"])

        plt.show()

    def plot_scf_convergence(self):
        """
        Plots SCF energy, Force and displacement from optimisation.
        :return:
        """
        fig = plt.figure()

        scf_data = fig.add_subplot(2, 4, (1, 6))
        scf_data.set_title("Energy")
        scf_data.plot(self.g_data["SCF Done"], label="SCF")
        plt.legend()

        force = fig.add_subplot(2,4,(3,4))
        force.set_title("Force")
        force.plot(self.g_data["Maximum Force"], label="Maximum")
        force.plot(self.g_data["RMS     Force"], label="RMS")
        plt.legend()

        displ = fig.add_subplot(2,4,(7,8))
        displ.set_title("Displacement")
        displ.plot(self.g_data["Maximum Displacement"], label="Maximum")
        displ.plot(self.g_data["RMS     Displacement"], label="RMS")
        plt.legend()

        fig.suptitle(self.filename)

        #plt.tight_layout()

        plt.show()