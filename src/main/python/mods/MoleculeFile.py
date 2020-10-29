from mods.GaussianFile import GaussianFile
from mods.Atoms import Atom, GaussianAtom


class XYZFile(GaussianFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        #Atom X Y Z
        # atoms = {1: {name: C, x:value, y: value, z: value}} --> atoms[index][x]
        self.atoms = dict()

        print(self.file_path)
        print(Atom.get_x)



    def read_coordinate(self):
        """
        :return:
        """
        # decide what type of file and send to correct reader

    def read_gout(self):
        """
        Extract xyz from a gaussian output file
        :return:
        """
        pass

    def read_ginp(self):
        """
        Extract coordinates from gaussian input file
        :return:
        """
        pass

    def read_pure_xyz(self):
        """
        Get coordinates from a pure .xyz file
        :return:
        """
        pass

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
