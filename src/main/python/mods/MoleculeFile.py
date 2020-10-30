from mods.GaussianFile import GaussianFile
from mods.Atoms import GaussianAtom


class XYZFile(GaussianFile):
    def __init__(self, atoms=None, filepath=None):
        #Atom X Y Z
        # atoms = {1: {name: C, x:value, y: value, z: value}} --> atoms[index][x]
        if atoms:
            self.atoms = atoms
        else:
            # read_xyz and fill self.atoms TODO
            self.atoms = self.read_xyz(filepath)


        super().__init__()

    @property
    def get_molecule(self):
        return self.atoms

    @property
    def get_formatted_xyz(self):
        molecule_xyz = list()

        for i in sorted(self.atoms.keys()):
            xyz_line = " %15s%14.8f%14.8f%14.8f" % (self.atoms[i]["name"].ljust(15),
                                                    self.atoms[i]["x"], self.atoms[i]["y"], self.atoms[i]["z"])
            molecule_xyz.append(xyz_line)

        return molecule_xyz

    def read_xyz(self, filepath):
        """
        :param filepath:
        :return:
        """
        # TODO
        return dict()

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

        super().__init__(atoms=self.g_molecule)

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

        return molecule

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
