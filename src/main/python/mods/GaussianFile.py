import distutils.util


class GaussianFile:
    def __init__(self, file_path):
        self.file_path = file_path

        self.job_details = dict

    def get_filepath(self):
        """
        Return: filepath for gaussianfile
        """
        return self.file_path


class InputFile(GaussianFile):

    def __init__(self, file_path):
        super().__init__(file_path)

        # Initialize dictionaries


class OutputFile(InputFile):

    def __init__(self, file_path):
        super().__init__(file_path)

        self.file_path = file_path

        # Job converged or not?
        self.converged = {"Maximum Force": bool,
                          "RMS     Force": bool,
                          "Maximum Displacement": bool,
                          "RMS     Displacement": bool}

        # Where to get gaussian output value from line.split(int)
        # first key = Line to look for in output file
        # second key(s) are key names for assignment in self.g_outdata with tuple value giving index [0] and
        # type expected in line [1]
        self.g_reader = {"Solvent":
                            {"Solvent": (2, str),
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

        #This will store data from output file given by self.g_reader
        self.g_outdata = dict()

        # Read output on init to get key job details
        self.read_gaussian_out()

    def read_gaussian_out(self):
        """
        Reads through Gaussian output file and assigns values to self.g_outdata using self.g_reader.
        """
        DFT_out = self.file_path
        with open(DFT_out) as f:
            for line in f:
                #Check if line contains any self.g_reader keys:
                if any(g_key in line for g_key in self.g_reader.keys()):
                    g_key = [term for term in self.g_reader.keys() if term in line][0]
                    for out_name in self.g_reader[g_key].keys():
                        split_int, type_ = self.g_reader[g_key][out_name][0:2]
                        line_value = line.split()[split_int]
                        if type_ is bool:
                            line_value = bool(distutils.util.strtobool(line_value))
                        else:
                            line_value = type_(line_value)

                        self.g_outdata[out_name] = line_value

    def check_convergence(self):
        """
        Returns True if all 4 SCF convergence criterias are met - else False
        :return: None (not geometry optimization), False (not converged) or True (converged)
        """
        converged = None

        converge_terms = list()
        for entry in self.g_outdata.keys():
            if "Converged?" in entry:
                converge_terms.append(self.g_outdata[entry])

        if len(converge_terms) > 3:
            if sum(converged_ is True for converged_ in converge_terms) == 4:
                converged = True
            else:
                converged = False

        return converged

    def get_energy(self):
        """
        :return: final SCF Done energy stored in self.g_outdata
        """
        return self.g_outdata["SCF Done"]

    def get_scf_convergence(self):
        """
        Reads output file and returns all SCF Done energies
        :return: energies, MaximumForce, RMS Force, Maximum Displacement, RMS Displacement
        """
