class GaussianFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_filepath(self):
        """
        Return: filepath for gaussianfile
        """
        return self.file_path


class InputFile(GaussianFile):

    def __init__(self, file_path):
        super().__init__(file_path)

        # Initialize dictionaries
        self.job_details = {}


class OutputFile(InputFile):

    def __init__(self, file_path):
        super().__init__(file_path)

        self.file_path = file_path

        self.ene = {}
        self.solvent = {}

        # Job converged or not?
        self.converged = {"Maximum Force": bool,
                          "RMS     Force": bool,
                          "Maximum Displacement": bool,
                          "RMS     Displacement": bool}

        # Where to get gaussian output value from line.split(int)
        # first key = Line to look for in output file
        # second key(s) are key names for assignment in self.job_details with tuple value giving index [0] and
        # type expected in line [1]
        self.g_reader = {"Solvent":
                            {"Solvent": (2, float),
                             "Eps": (4, float)},
                        "SCF Done":
                            {"SCF Done": (4, float)},
                        "Zero-point correction=":
                            {"Zero-point correction": (2, float)},
                        "Thermal correction to Energy= ":
                            {"Thermal correction to Energy": (4, float)},
                        "Thermal correction to Enthalpy":
                            {"Thermal correction to Enthalpy": (4, float)},
                        "Thermal correction to Gibbs Free Energy":
                            {"Thermal correction to Gibbs Free Energy": (6, float)},
                        "Maximum Force":
                             {"Maximum Force Value": (2, float),
                              "Maximum Force Threshold": (3, float),
                              "Maximum Force Converged?": (4, bool)},
                        "RMS     Force":
                             {"RMS Force Value": (2, float),
                              "RMS Force Threshold": (3, float),
                              "RMS Force Converged?": (4, bool)},
                        "Maximum Displacement":
                             {"Maximum Displacement Value": (2, float),
                              "Maximum Displacement Threshold": (3, float),
                              "Maximum Displacement Converged?": (4, bool)},
                        "RMS     Displacement":
                             {"RMS Displacement Value": (2, float),
                              "RMS Displacement Threshold": (3, float),
                              "RMS Displacement Converged?": (4, bool)}
                        }

        # Read output on init to get key job details
        self.read_gaussian_out()

    def read_gaussian_out(self):
        """

        """
        DFT_out = self.file_path
        with open(DFT_out) as f:
            # TODO init globals with None/False
            for line in f:

                if "Solvent" in line:
                    self.phase = line.split()[2]
                    self.Eps = "{:.2f}".format(float(line.split()[4]))

                if "SCF Done" in line:
                    self.ene["energy"] = float(line.split()[4])

                if "Zero-point correction=" in line:
                    self.ene["ZPE"] = float(line.split()[2])

                elif "Thermal correction to Energy= " in line:
                    self.ene["dE"] = float(line.split()[4])

                elif "Thermal correction to Enthalpy=" in line:
                    self.ene["dH"] = float(line.split()[4])

                elif "Thermal correction to Gibbs Free Energy=" in line:
                    self.ene["dG"] = float(line.split()[6])

                # Check convergence:
                for term in self.converged.keys():
                    if term in line:
                        if line.split()[4] == "YES":
                            self.converged[term] = True
                        else:
                            self.converged[term] = False

    def check_convergence(self):
        """
        Returns True if all 4 SCF convergence criterias are met - else False
        :return: None (not geometry optimization), False (not converged) or True (converged)
        """
        if None in self.converged.values():
            converged = None
        else:
            converged = False
            if sum(term is True for term in self.converged.values()) == 4:
                converged = True

        return converged

    def get_energy(self):
        """
        :return:
        """
        return self.ene["energy"]

    def get_scf_convergence(self):
        """
        Reads output file and returns all SCF Done energies
        :return: energies, MaximumForce, RMS Force, Maximum Displacement, RMS Displacement
        """
