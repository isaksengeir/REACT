import os


hiddenimports = list()

print("hello")
for file_ in os.listdir():
    filename = os.fsdecode(file_)
    if filename.endswith(".py"):
        hiddenimports.append("../pmg_qt/%s" % file_ )

print(hiddenimports)
