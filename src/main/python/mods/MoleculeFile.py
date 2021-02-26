#from mods.GaussianFile import GaussianFile
from mods.Atoms import XYZAtom, GaussianAtom, PDBAtom


class XYZFile:
    def __init__(self, molecule=None, atoms=None, filepath=None):
        #Atoms = list(Atom)
        # molecule = {1: {name: C, x:value, y: value, z: value}} --> atoms[index][x]
        if molecule:
            self.molecule = molecule

        if atoms:
            # List of Atom objects
            self.atoms = atoms

        if filepath:
            # read_xyz and fill self.atoms TODO
            self.atoms = self.read_xyz(filepath)

        if not molecule:
            self.molecule = self.make_molecule()

    @property
    def get_molecule(self):
        return self.molecule

    @property
    def get_formatted_xyz(self):
        molecule_xyz = list()

        for i in sorted(self.molecule.keys()):
            xyz_line = " %15s%14.8f%14.8f%14.8f" % (self.molecule[i]["name"].ljust(15),
                                                    self.molecule[i]["x"], self.molecule[i]["y"], self.molecule[i]["z"])
            molecule_xyz.append(xyz_line)

        return molecule_xyz

    def read_xyz(self, filepath):
        """
        :param filepath: path to xyz file
        :return: dict with atoms - {atom_index: {name: C, x:value, y: value, z: value}}
        """
        index = 0
        atoms = list()
        with open(filepath, "r") as xyz:
            for line in xyz:
                if len(line.split()) > 3:
                    index += 1
                    atoms.append(XYZAtom(line, index))
        return atoms

    def make_molecule(self):
        molecule = dict()
        for i in range(len(self.atoms)):
            atom = self.atoms[i]
            atom_index = atom.get_atom_index
            molecule[atom_index] = dict()
            molecule[atom_index]["name"] = atom.get_atom_name
            molecule[atom_index]["x"] = atom.get_x
            molecule[atom_index]["y"] = atom.get_y
            molecule[atom_index]["z"] = atom.get_z

        return molecule

    def convert_to_pdb(self):
        """
        Create PDB file from XYZ file
        :return: TODO
        """
        pass


class GaussianMolecule(XYZFile, GaussianAtom):
    """
    Takes a list of GaussianAtom or Atom objects and creates a molecule
    """
    def __init__(self, g_atoms):
        self.g_atoms = g_atoms

        super().__init__(atoms=self.g_atoms)

    # TODO Gaussian molecule probably need some unique properties not present in XYZ file


class PDBFile(XYZFile, PDBAtom):
    def __init__(self, pdb_atoms=None, filepath=None):
        if filepath:
            self.atoms = self.read_pdb(filepath)
        elif pdb_atoms:
            self.atoms = pdb_atoms

        super().__init__(atoms=self.atoms)

    def read_pdb(self, filepath):
        atoms = list()
        with open(filepath, "r") as pdb:
            for line in pdb:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    atoms.append(PDBAtom(line))
        return atoms

    def convert_to_xyz(self):
        """
        Create XYZ file from PDB file
        :return: TODO
        """
        pass
