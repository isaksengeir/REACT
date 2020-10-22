

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

        #Initialize dictionaries
        self.job_details = {}


class OutputFile(InputFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.ene = {}
        self.solvent = {}
        self.converged = {"Maximum Force": None,
                          "RMS     Force": None,
                          "Maximum Displacement": None,
                          "RMS     Displacement": None}

        #Read output
        self.read_dft_out(file_path)
        #TODO check convergence and analyse file

    def read_dft_out(self, DFT_out):
        """ Very unfinished code, should also be moved to a GaussianOUT class
        """
    
        with open(DFT_out) as f:
             #TODO init globals with None/False
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

                #Check convergence:
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
            if sum(term == True for term in self.converged.values()) == 4:
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



