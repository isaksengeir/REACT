#!/usr/bin/env python
import sys
import copy
import numpy as np


class AtomBond():
    """
    Class to represent the atom bond that is to be scanned.
    Atom1 will be kept frozen while scan (except if move both == True)
    """

    def __init__(self, xyz, atom1_idx, atom2_idx, bond_dist, scan_dist, step_size, move_both, scan_mode):
        self._atom1_idx = atom1_idx
        self._atom2_idx = atom2_idx
        self.xyz = self.convert_xyz(xyz)
        self._bond_dist = bond_dist
        self._scan_dist = scan_dist
        self._step_size = step_size
        self.num_atoms = len(xyz)
        self._move_both = move_both
        self._scan_mode = scan_mode

    def invert_atoms(self):
        temp = self.atom1_idx
        self.atom1_idx = self.atom2_idx
        self.atom2_idx = temp 

    def get_dist(self, atomA, atomB):
        vector = np.array([atomB['x']-atomA['x'], atomB['y']-atomA['y'], atomB['z']-atomA['z']])
        return np.linalg.norm(vector)

    def convert_xyz(self, xyz):
        """
        Convert coordinates into the data format used within this class
        """
        i = 0
        atoms = {}

        for entry in xyz:
            temp = entry.split()
            element = temp[0]
            x = float(temp[1])
            y = float(temp[2])
            z = float(temp[3])

            atoms[i] = {'element': element, 'x': x, 'y': y, 'z': z}
            i += 1

        return atoms

    def convert_back(self, atoms):
        """
        Convert coordinates back into format of mol_obj.formatted_xyz
        """
        i = 0

        all_atoms = []

        for i in range(self.num_atoms):
            all_atoms.append([atoms[i]['element'], format(atoms[i]['x'], ".8f"),
                              format(atoms[i]['y'],".8f"), format(atoms[i]['z'], ".8f")])

        return all_atoms

    def move_atom(self, atom, vector, weight):
        """
        Given a vector, move atom along the vector, with magnitude = weight
        """

        x = atom['x']
        y = atom['y']
        z = atom['z']

        return {'element': atom['element'],
                'x': x + (vector['a'] * weight),
                'y': y + (vector['b'] * weight),
                'z': z + (vector['c'] * weight)}

    def calc_abc_values(self, atom1, atom2, dist):
        """
        abc values are x,y,z values (respectively) to the vector going FROM
        atom1 and TO atom2
        """
        a = ((atom2['x'] - atom1['x'])/dist)
        b = ((atom2['y'] - atom1['y'])/dist)  
        c = ((atom2['z'] - atom1['z'])/dist)

        return {'a': a, 'b': b, 'c': c}

    def update_xyz(self, all_xyz, atom_idx, new_atom_xyz):
        """
        Update xyz of one atom.
        """
        new_xyz = copy.deepcopy(all_xyz)
        new_xyz[atom_idx] = new_atom_xyz

        return new_xyz

    def scan_bond(self, atom1_idx, atom2_idx, xyz):
        """
        First, calcuate the vector moving from atom1 and to atom2.
        Fetch the coordinates of atom1 and atom2 (atom*_forv, atom*_rev)
        Some of these variables will be used in proceeding loop, where 
        the coordiantes are updated(one step) for each loop.
        In every loop, a new set of all coordinates are appended to a list.
        In the end, this list is returned.
        """
        abc_vector = self.calc_abc_values(xyz[atom1_idx], xyz[atom2_idx], self.bond_dist)

        atom1_forw = xyz[atom1_idx]
        atom1_rev = xyz[atom1_idx]
        atom2_forw = xyz[atom2_idx]
        atom2_rev = xyz[atom2_idx]

        xyz_extend_bond = [xyz]
        xyz_decrease_bond = []

        steps = int(self.scan_dist/self.step_size)

        if self.move_both == True:

            for i in range(steps):
                atom1_forw = self.move_atom(atom1_forw, abc_vector, (self.step_size * 0.5))
                atom2_rev = self.move_atom(atom2_rev, abc_vector, (self.step_size * -0.5))

                atom1_rev = self.move_atom(atom1_rev, abc_vector, (self.step_size * -0.5))
                atom2_forw = self.move_atom(atom2_forw, abc_vector, (self.step_size * 0.5))

                temp = self.update_xyz(xyz, atom1_idx, atom1_forw)
                xyz_decrease_bond.append(self.update_xyz(temp, atom2_idx, atom2_rev))

                temp = self.update_xyz(xyz, atom1_idx, atom1_rev)
                xyz_extend_bond.append(self.update_xyz(temp, atom2_idx, atom2_forw))

            xyz_extend_bond.reverse()
            xyz_extend_bond.extend(xyz_decrease_bond)

            return xyz_extend_bond

        else:
            for i in range(steps):
                atom2_forw = self.move_atom(atom2_forw, abc_vector, self.step_size)
                atom2_rev = self.move_atom(atom2_rev, abc_vector, (self.step_size * -1))

                xyz_extend_bond.append(self.update_xyz(xyz, atom2_idx, atom2_forw))
                xyz_decrease_bond.append(self.update_xyz(xyz, atom2_idx, atom2_rev))

            xyz_decrease_bond.reverse()
            xyz_decrease_bond.extend(xyz_extend_bond)

            return xyz_decrease_bond

    def write_xyzfiles(self, path, filename_in=False):
        """
        Write all xyz as .xyz files
        """
        self.all_xyz = self.scan_bond(self.atom1_idx-1, self.atom2_idx-1, self.xyz)

        for i in range(len(self.all_xyz)):
            xyz = self.convert_back(self.all_xyz[i])

            if not filename_in:
                filename = f"scan_{i:02d}.xyz"
            else:
                return
                pass #TODO

            with open(path + filename, "w+") as f:
                for item in xyz:

                    whitespaces = []

                    if item[1][0] == '-':
                        whitespaces.append('     ')
                    else:
                        whitespaces.append('      ')
                    if item[2][0] == '-':
                        whitespaces.append('  ')
                    else:
                        whitespaces.append('   ')
                    if item[3][0] == '-':
                        whitespaces.append('  ')
                    else:
                        whitespaces.append('   ')

                    #length of whitespace + xyz = 7
                    atom = [None]*(7)
                    atom[::2] = item
                    atom[1::2] = whitespaces
                    
                    f.write("   ".join(atom) + "\n")

    @property
    def atom1_idx(self):
        return self._atom1_idx

    @atom1_idx.setter
    def atom1_idx(self, value):
        self._atom1_idx = value

    @property
    def atom2_idx(self):
        return self._atom2_idx

    @atom2_idx.setter
    def atom2_idx(self, value):
        self._atom2_idx = value

    @property
    def bond_dist(self):
        return self._bond_dist

    @bond_dist.setter
    def bond_dist(self, value):
        self._bond_dist = value

    @property
    def scan_dist(self):
        return self._scan_dist

    @scan_dist.setter
    def scan_dist(self, value):
        self._scan_dist = value

    @property
    def step_size(self):
        return self._step_size

    @step_size.setter
    def step_size(self, value):
        self._step_size = value

    @property
    def scan_mode(self):
        return self._scan_mode

    @scan_mode.setter
    def scan_mode(self, value):
        self._scan_mode = value

    @property
    def move_both(self):
        return self._move_both

    @move_both.setter
    def move_both(self, value):
        self._move_both = value

if __name__ == '__main__':

    all_xyz = []

    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = line.replace("\n", "")
            all_xyz.append(line)

    #AtomBond(all_xyz, 10, 78, 0.5, 0.2, move_both=False)
       