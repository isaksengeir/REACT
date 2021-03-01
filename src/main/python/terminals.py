###
from mods.MoleculeFile import PDBFile
from mods.Atoms import PDBAtom, Atom
from mods.common_functions import atom_distance

pdb_path = "../resources/DFT_testfiles/cluster2.pdb"

"""
1. Create a PDBFile instance
2. Compute distances for relevant atoms (C and N pdb atom names.... ACE/NME, or MET... or just check all...)
"""

pdb = PDBFile(filepath=pdb_path)

atoms = pdb.atoms

freeze = list()
expected = ["CA", "C", "H", "N", "O"]

for atom in atoms:
    pdb_name = atom.get_pdb_atom_name
    if pdb_name in ["C", "N"]:
        atoms.pop(0)
        for next_atom in atoms:
            radius = atom_distance(atom.get_coordinate, next_atom.get_coordinate)
            if radius < 1.7:
                if next_atom.get_pdb_atom_name not in expected:
                    freeze.append(next_atom.get_atom_index)

print(freeze)


