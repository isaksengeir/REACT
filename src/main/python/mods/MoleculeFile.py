from mods.GaussianFile import GaussianFile


class XYZFile(GaussianFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        #Atom X Y Z
        #atoms = {1:}


class PDBFile(GaussianFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        #ATOM
        #Atom number
        #PDB ATOM NAME
        #Residue name
        #Residue Number
