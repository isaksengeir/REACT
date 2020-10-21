class GaussianFile():
    def __init__(self, file_path):
    
        self.file_path = file_path
        self.job_details = {}
        self.ene = {}

        self.read_dft_out(file_path)
        #TODO check convergence and analyse file

    def get_filepath(self):
        """
        Return: filepath for gaussianfile
        """
        return self.file_path

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
                    self.ene["E_energy"] = float(line.split()[4])
                    
                if "Zero-point correction=" in line:
                    self.ene["ZPE"] = float(line.split()[2])
                    
                elif "Thermal correction to Energy= " in line:
                    self.ene["dE"] = float(line.split()[4])

                elif "Thermal correction to Enthalpy=" in line:
                    self.ene["dH"] = float(line.split()[4])

                elif "Thermal correction to Gibbs Free Energy=" in line:
                    self.ene["dG"] = float(line.split()[6])

    def get_energy(self):
         return self.ene["energy"]