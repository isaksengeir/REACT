from mods.GaussianFile import GaussianFile
from mods.Atoms import GaussianAtom


class XYZFile():
    def __init__(self, atoms = None):
        #Atom X Y Z
        # atoms = {1: {name: C, x:value, y: value, z: value}} --> atoms[index][x]
        if atoms:
            self.atoms = atoms
        else:
            self.atoms = dict()

    def get_formatted_xyz(self):

    def convert_to_pdb(self):
        """
        Create PDB file from XYZ file
        :return: TODO
        """
        pass


class GaussianMolecule(XYZFile, GaussianAtom):
    """
    Takes a list of GaussianAtoms
    """
    def __init__(self, g_atoms):
        self.g_molecule = self.make_molecule(g_atoms)

        super().__init__(self.g_molecule)

    def make_molecule(self, g_atoms):
        molecule = dict()
        for i in range(len(g_atoms)):
            atom = g_atoms[i]
            atom_index = atom.get_atom_index
            molecule[atom_index] = dict()
            molecule[atom_index]["name"] = atom.get_atom_name
            molecule[atom_index]["x"] = atom.get_x
            molecule[atom_index]["y"] = atom.get_y
            molecule[atom_index]["z"] = atom.get_z

    # TODO Gaussian molecule probably need some unique properties not present in XYZ file

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
