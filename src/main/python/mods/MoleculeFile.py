from mods.GaussianFile import GaussianFile


class XYZFile(GaussianFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        #Atom X Y Z
        # atoms = {1: {name: C, x:value, y: value, z: value}} --> atoms[index][x]
        self.atoms = dict()

        print(self.file_path)

        # Atom number to atom dictionary - only most common elements. Maybe complete at some point later ... maybe not.
        self.atom_nr_atom = {1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8:"O", 9: "F", 10: "Ne",
                             11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K",
                             20: "Ca", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn", 34: "Se",
                             35: "Br", 36: "Kr", 53: "I"}

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
