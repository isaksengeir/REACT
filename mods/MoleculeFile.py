from mods.Atoms import XYZAtom, GaussianAtom, PDBAtom


class Molecule:
    """
    Takes a list of Atom objects at init and creates molecule (dict)
    molecule[i] = Atom
    """
    def __init__(self, atoms=None):
        self._molecule = dict()
        if atoms:
            if isinstance(atoms, dict):
                self._molecule = self.atoms
                self.atoms = self.atoms.values()
            else:
                self.atoms = atoms
                self.make_molecule()

    def make_molecule(self):
        for i in range(len(self.atoms)):
            self._molecule[i+1] = self.atoms[i]

    @property
    def molecule(self):
        return self._molecule

    @property
    def formatted_xyz(self):
        molecule_xyz = list()

        for i in sorted(self.molecule.keys()):
            molecule_xyz.append(self.molecule[i].formatted_xyz)

        return molecule_xyz

    @property
    def atom_count(self):
        return len(self.atoms)

    @molecule.setter
    def molecule(self, value):
        self._molecule = value

    def convert_to_pdb(self):
        """
        Create PDB file from XYZ file
        :return: TODO ?
        """
        pass


class XYZFile(Molecule):
    def __init__(self, atoms=None, filepath=None):
        # Atoms = list(Atom)
        if atoms:
            # List of Atom objects
            self.atoms = atoms

        if filepath:
            self._filepath = filepath
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

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value


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


class Geometries(XYZFile):
    """
    Takes a list of molecules [[Atoms], [Atoms],... iterations SCF] typically from geometry optimisations.
    """
    def __init__(self, molecules, filepath=None):

        # [[Atoms], [Atoms],... iterations SCF]
        self._molecules = molecules

        # Init with final molecule / geometry optimization
        super().__init__(atoms=self.final_molecule, filepath=filepath)

    @property
    def count_molecules(self):
        return len(self._molecules)

    @property
    def final_molecule(self):
        return self._molecules[-1]
