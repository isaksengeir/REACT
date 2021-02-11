class Atom:
    """
    Class to store information for atoms.
    Coordinates, mass, name, pdb name, type etc.
    """
    def __init__(self, atom, x, y, z, index=None):
        # Atom number to atom dictionary - only most common elements. Maybe complete at some point later ... maybe not.
        self.atomnr_atom = {1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne",
                             11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K",
                             20: "Ca", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn", 34: "Se",
                             35: "Br", 36: "Kr", 53: "I"}

        # Atom name to atom number dictionary
        self.atom_atomnr = {atom: atomnr for atomnr, atom in self.atomnr_atom.items()}

        # TODO make a dictionary for atom mass as well

        #atom can be passed to Atom class either as atomic number or atomic name:
        if atom.isdigit():
            self.atomnr = int(atom)
            self.atomname = self.atomnr_atom[self.atomnr]
        else:
            self.atomnr = self.atom_atomnr[atom]
            self.atomname = atom

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

        if index:
            self.center_number = index

    @property
    def get_x(self):
        return self.x

    @property
    def get_y(self):
        return self.y

    @property
    def get_z(self):
        return self.z

    @property
    def get_coordinate(self):
        coordinates = (self.x, self.y, self.z)
        return coordinates

    @property
    def get_atom_name(self):
        return self.atomname

    @property
    def get_atom_nr(self):
        return self.atomnr

    @property
    def get_atom_index(self):
        return int(self.center_number)


class GaussianAtom(Atom):
    """
    Class to store information for atom coordinates extracted from Gaussian output files.
    takes line from gaussian file and converts it into GaussianAtom object, where atom_line:
    Center     Atomic      Atomic             Coordinates (Angstroms)
    Number     Number       Type             X           Y           Z
     1          6           0       -3.809685    3.412407   -1.222092
    """
    def __init__(self, atom_line=None):
        if atom_line:
            # Gaussian atom attributes:
            self.center_number = int(atom_line.split()[0])
            self.atomic_type = int(atom_line.split()[2])

            # Atom class attributes:
            atom_nr = atom_line.split()[1]
            x_coordinate = float(atom_line.split()[3])
            y_coordinate = float(atom_line.split()[4])
            z_coordinate = float(atom_line.split()[5])
            super(GaussianAtom, self).__init__(atom_nr, x_coordinate, y_coordinate, z_coordinate)

        # atom = {index: int, name: C:str, X:float, Y:float, Z:float}


class PDBAtom(Atom):
    """
    Subclass of the Atom class with additional info required by the PDB file format TODO
    """
    def __init__(self):
        pass
        super(PDBAtom, self).__init__()
        pass
