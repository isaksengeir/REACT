import distutils.util
from mods.Atoms import GaussianAtom


class GaussianFile:
    def __init__(self, file_path=None):
        if file_path:
            self.file_path = file_path

        # TODO Put in some defaults here for now:
        self.job_details = dict()
        self.set_default_settings()

    def set_default_settings(self):
        """
        TODO get settings from global settings (should be stored in a file, and read from there probably)
        :return:
        """
        self.job_details["basis set"] = "6-31g(d,p)"
        self.job_details["DFT functional"] = "b3lyp"
        self.job_details["modredundant"] = True
        self.job_details["empiricaldispersion"] = "gd3"

    @property
    def get_basis(self):
        return self.job_details["basis set"]

    @property
    def get_dft_functional(self):
        return self.job_details["DFT functional"]

    @property
    def get_filepath(self):
        """
        Return: filepath for gaussianfile
        """
        return self.file_path


    def update_fileobject(self):
        """
        TODO Called after file has been edited in text editor, should update object accordingly to changes in file. 
        """
        pass

class InputFile(GaussianFile):

    def __init__(self, file_path):
        super().__init__(file_path)

        # Initialize dictionaries TODO:
        # Job Types: Energy, Optimization, Frequency, Opt+Freq, IRC, Scan
        # optimize to: Minimum, TS
        # Use tight convergence criteria: False (True: opt=tight)
        # Force Constants: default, Calculate at First point (opt=calcf), Calculate at all points (opt=calcall)
        # Method: Ground state ... there are other, but stick with this for now
        # Method type: DFT (include HF, MP2, MP4?)
        # Method functional: B3LYP
        # Spin type: Default Spin, Restricted, Undrestricted, Restricted-Open
        # multiplicity = 2S+1 (S=1/2*n; where n is number of unpaired electrons). For molecules and ions, S=0!
        # Spin multiplicity: Singlet, Triplet
        # Charge: 0 #Todo write method to find charge of molecule?
        # Basis set: 6-31G+(d,p)
        # Additional keywords: # Todo make this more elegant than GaussView opt=noeigentest, empiricaldispersion=gd3 ..
        # Job title: my job
        # memory: 16GB
        # Shared processors: None (None = do not include in input file)
        # Checkpoint file: None
        # Old checkpoint file: None
        # Quadratic convergent SCF: False (True = scf=qc)
        # Use modified redundant coordinates: False (opt=modredundant)
        # Compute polarizabilities: False (True = polar)
        # Additional print: True (# at beginning of inputfile line)
        # Solvation model: None, CPCM, IEFPCM, SMD
        # solvent: default, Water, DMSO, Methanol, Ethanol ....
        # Eps: None (default for solvent), number (include read at top and eps=number at end of input file)
        job_options = {"Job type": "Energy"}


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
                        if type_ is bool:
                            line_value = bool(distutils.util.strtobool(line.split()[split_int]))
                        else:
                            line_value = type_(line.split()[split_int])

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

    @property
    def get_energy(self):
        """
        :return: final SCF Done energy stored in self.g_outdata
        """
        return self.g_outdata["SCF Done"]

    @property
    def get_scf_convergence(self):
        """
        Reads output file and returns all SCF Done energies
        :return: energies, MaximumForce, RMS Force, Maximum Displacement, RMS Displacement
        """
        # SCF Done 4
        scf = list()

        # "Maximum Force" 2
        max_force = list()

        # "RMS     Force" 2
        rms_force = list()

        # "Maximum Displacement" 2
        max_displacement = list()

        # "RMS     Displacement" 2
        rms_displacement = list()
        scf_data = {"SCF Done": list(),
                    "Maximum Force": list(),
                    "RMS     Force": list(),
                    "Maximum Displacement": list(),
                    "RMS     Displacement": list()}

        with open(self.file_path) as out:
            for line in out:
                if any(g_key in line for g_key in scf_data.keys()):
                    g_key = [term for term in scf_data.keys() if term in line][0]
                    split_int = 2
                    if g_key == "SCF Done":
                        split_int = 4
                    scf_data[g_key].append(float(line.split()[split_int]))

        return scf_data

    @property
    def get_coordinates(self):
        """
        Extract xyz from a gaussian output file and creates GaussianAtom objects

        :return: iter_atoms = [ [iteration 1], [iteration 2], .... ] where [iteration 1] = [GaussianAtom1, ....]
        """
        # list with GaussianAtom objects per geometry optimization --> iter_atoms[-1] is the final atom coordinates
        iter_atoms = list()

        atoms = list()
        with open(self.file_path, 'r') as gout:
            standard_orientation = False
            get_coordinates = False
            for line in gout:
                if standard_orientation and line.split()[0].isdigit():
                    get_coordinates = True

                if get_coordinates:
                    if not line.split()[0].isdigit():
                        standard_orientation = False
                        get_coordinates = False

                        iter_atoms.append(atoms)
                    else:
                        atoms.append(GaussianAtom(line))

                if "Standard orientation" in line:
                    standard_orientation = True
                    atoms = list()

        return iter_atoms


