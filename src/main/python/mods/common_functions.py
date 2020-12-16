from PyQt5.QtWidgets import QColorDialog
import random

unicode_symbols = {"delta": "\u03B4", "Delta": "\u0394"}


def random_color():
    """
    :return: Hex Color Code
    """
    return f"#{random.randrange(0x1000000):06x}"


def select_color(parent=None):
    """
    Opens QColorDialog where user selects color.
    :return: Hex Color Code
    """
    color = QColorDialog.getColor(parent=parent)
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
