from mods.GaussianFile import GaussianFile


class XYZFile(GaussianFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        #Atom X Y Z
        #atoms = {1:}

    def convert_to_pdb(self):
        """
        Create PDB file from XYZ file
        :return: TODO
        """
        pass


class PDBFile(GaussianFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        #ATOM
        #Atom number
        #PDB ATOM NAME
        #Residue name
        #Residue Number

    def convert_to_xyz(self):
        """
        Create XYZ file from PDB file
        :return: TODO
        """
        pass
