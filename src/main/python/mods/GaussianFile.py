class GaussianFile():
    def __init__(self, file_path):
    
        self.file_path = file_path
        self.job_details = {}
        self.ene = {}
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
            
            for line in f:

                if "Solvent" in line:
                    self.phase = line.split()[2]
                    self.Eps = float("{:.2f}".format(line.split()[4]))

                if "SCF Done" in line:
                    self.ene["E_gas"] = float(line.split()[4])
                    
                if "Zero-point correction=" in line:
                    self.ene["ZPE"] = float(line.split()[2])
                    
                elif "Thermal correction to Energy= " in line:
                    self.ene["dE"] = float(line.split()[4])

                elif "Thermal correction to Enthalpy=" in line:
                    self.ene["dH"] = float(line.split()[4])

                elif "Thermal correction to Gibbs Free Energy=" in line:
                    self.ene["dG"] = float(line.split()[6])