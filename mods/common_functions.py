from PyQt5.QtWidgets import QColorDialog
import random
import numpy as np
import json

unicode_symbols = {"delta": "\u03B4", "Delta": "\u0394"}


def random_color():
    """
    :return: Hex Color Code
    """
    return f"#{random.randrange(0x1000000):06x}"


def select_color(parent=None, return_hex=True):
    """
    Opens QColorDialog where user selects color.
    :return_hex: Return hex color code
    :return: Hex Color Code (hex=True), else RGB tuple will be returned (r,g,b)
    """
    color = QColorDialog.getColor(parent=parent)
    if return_hex:
        return color
    else:
        color = color.lstrip("#")
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))


def hartree_to_kcal(au):
    """
    :param au: Hartree /atomic units
    :return: kcal
    """
    return float(au) * 627.51


def hartree_to_kjoul(au):
    """
    :param au: Hartree /atomic units
    :return: kjoul
    """
    return float(au) * 2625.51


def is_number(s):
    """
    Check if string is a float value
    :param s: string or anything
    :return: True/False for s is float
    """
    try:
        float(s)
        return True
    except:
        return False


def json_hook_int_bool_converter(obj):
    """
    Used as object hook when calling json.load()
    Will convert a key-object of type str into type int, if possible
    """
    new_dict = {}
    for k, v in obj.items():
        if isinstance(v, dict):
            new_dict_sub = {}
            for k_sub, v_sub in v.items():
            
                if v_sub == 'false':
                    new_dict_sub[k_sub] = False
                elif v_sub == 'true':
                    new_dict_sub[k_sub] = True

                else: 
                    try: 
                        new_k_sub = int(k_sub)
                        new_dict_sub[new_k_sub] = v[k_sub]
                    except ValueError:
                        new_dict_sub[k] = v[k_sub]

            new_dict[k] = new_dict_sub

        if v == 'false':
            new_dict[k] = False
        elif v == 'true':
            new_dict[k] = True
        else:
            try:
                new_k = int(k)
                new_dict[new_k] = obj[k]
            except ValueError:
                new_dict[k] = obj[k]
        
    return new_dict


def load_json(json_path, json_hook=False):
    with open(json_path, 'r') as json_file:
        obj = json.load(json_file, object_hook=json_hook)

    return obj


def dump_json(json_path, obj):
    with open(json_path, 'w') as json_file:
        json_file.dump(obj)


def write_file(list_stuff, path):
    """
    Takes a list of lines and writes file to path
    :param list_stuff: list()
    :param path: str()
    :return: path: str()
    """
    _file = open(path, "w")
    for line in list_stuff:
        _file.write(line + "\n")
    _file.close()


def find_ligands_pdbfile(pdbfile):
    """
    Reads through a PDB file and identifies residue_names that har not amino acids or similar. Used for highlighting
    ligands in pymol.
    :param pdbfile: path to pdb file.
    :return: resnames (list of non-protein residue names)
    """
    residues = list()

    res_ignore = ["GLY", "HIS", "HID", "HIP", "HIE", "ALA", "VAL", "ILE", "CYS", "MET", "TYR", "ASP", "GLU", "ARG",
                  "LYS", "PHE", "TRP", "ASN", "GLN", "SER", "AR+", "LY+", "GL-", "AS-", "PRO", "LEU", "THR"]
    # N-terminals (Q-style)
    res_ignore += ["N%s" % x for x in res_ignore]
    # C-terminals (Q-style)
    res_ignore += ["C%s" % x for x in res_ignore]
    # ions etc.
    res_ignore += ["CL-", "CLA", "HOH", "WAT", "Cl-", "SOD", "Na+", "NA+"]

    with open(pdbfile, "r") as pdb:
        for line in pdb:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                res = line[17:21].strip()
                if res not in res_ignore:
                    if res not in residues:
                        residues.append(res)

    return residues


def atom_distance(a1, a2):
    """
    :param a1: [x,y,z]
    :param a2: [x,y,z]
    :return: radois (float)
    """
    return np.sqrt((float(a2[0]) - float(a1[0]))**2 + (float(a2[1]) - float(a1[1]))**2 + (float(a2[2]) -
                                                                                          float(a1[2]))**2)
