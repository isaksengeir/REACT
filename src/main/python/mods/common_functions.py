from PyQt5.QtWidgets import QColorDialog
import random

unicode_symbols = {"delta": "\u03B4", "Delta": "\u0394"}


def random_color():
    """
    :return: Hex Color Code
    """
    return f"#{random.randrange(0x1000000):06x}"


def select_color():
    """
    Opens QColorDialog where user selects color.
    :return: Hex Color Code
    """
    color = QColorDialog.getColor()
    return color


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


def json_hook_int_please(obj):
    """
    Used as object hook when calling json.load()
    Will convert a key-object of type str into type int, if possible
    """
    new_dict = {}
    for k, v in obj.items():
        if isinstance(v,dict):
            new_dict_sub = {}
            for k_sub, v_sub in v.items():
                try: 
                    new_k_sub = int(k_sub)
                    new_dict_sub[new_k_sub] = v[k_sub]
                except ValueError:
                    new_dict_sub[k] = v[k_sub]
        try: 
            new_k = int(k)
            new_dict[new_k] = obj[k]
        except ValueError:
            new_dict[k] = obj[k]
        
    return new_dict