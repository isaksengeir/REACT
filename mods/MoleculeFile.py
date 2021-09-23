#from mods.GaussianFile import GaussianFile
from mods.Atoms import XYZAtom, GaussianAtom, PDBAtom


class Molecule:
    """
    Takes a list of Atom objects at init and creates molecule (dict)
    molecule[i] = Atom
    """
    def __init__(self, atoms=None):
        self.molecule = dict()
        if atoms:
            # TODO temporary fix here... in State.py or GaussianFile.py we pass a dictionary... re-implement to match..
            if isinstance(atoms, dict):
                self.molecule = self.atoms
                self.atoms = self.atoms.values()
            else:
                self.atoms = atoms
                self.make_molecule()

    def make_molecule(self):
        for i in range(len(self.atoms)):
            self.molecule[i+1] = self.atoms[i]

    @property
    def get_molecule(self):
        return self.molecule

    @property
    def get_formatted_xyz(self):
        molecule_xyz = list()

        for i in sorted(self.molecule.keys()):
            molecule_xyz.append(self.molecule[i].formatted_xyz)

        return molecule_xyz

    @property
    def get_atom_count(self):
        return len(self.atoms)


class XYZFile(Molecule):
    def __init__(self, atoms=None, filepath=None):
        #Atoms = list(Atom)
        if atoms:
            # List of Atom objects
            self.atoms = atoms

        if filepath:
            self.filepath = filepath
            self.atoms = self.read_xyz()

        super(XYZFile, self).__init__(atoms=self.atoms)

    def read_xyz(self):
        """
        :param filepath: path to xyz file
        :return: dict with atoms - {atom_index: {name: C, x:value, y: value, z: value}}
        """
        index = 0
        atoms = list()
        with open(self.filepath, "r") as xyz:
            for line in xyz:
                if len(line.split()) > 3:
                    index += 1
                    atoms.append(XYZAtom(line, index))
        return atoms

    def convert_to_pdb(self):
        """
        Create PDB file from XYZ file
        :return: TODO (maybe this belongs in Molecule parent)
        """
        pass

    @property
    def get_filepath(self):
        return self.filepath


class GaussianMolecule(XYZFile):
    """
    Takes a list of GaussianAtom or Atom objects and creates a molecule
    """
    def __init__(self, g_atoms):
        self.g_atoms = g_atoms

        super().__init__(atoms=self.g_atoms)

    # TODO Gaussian molecule probably need some unique properties not present in XYZ file


class PDBFile(XYZFile):
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

    @property
    def formatted_pdb(self):
        pdb_list = list()
        for i in sorted(self.molecule.keys()):
            pdb_list.append(self.molecule[i].get_pdb_line)
        return pdb_list




