import os

pymol_ = "/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol"

hiddenimports = list()

print("hello")
for file_ in os.listdir(pymol_):
    filename = os.fsdecode(file_)
    if filename.endswith(".py"):
        hiddenimports.append("pymol.%s" % filename.split(".")[0])

print(hiddenimports)
