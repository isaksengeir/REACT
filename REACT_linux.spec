# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None
file_path = os.getcwd()

a = Analysis(['REACT.py'],
             pathex=[f'{file_path}'],
             datas=[('/cluster/home/gvi022/software/REACT/OpenSourcePymol/dist/OpenSourcePymol', 'OpenSourcePymol/dist/') ],
             hiddenimports=["PyQt5.sip"],
             hookspath=[],
             runtime_hooks=[],
             excludes=["Qt4Agg", "TkAgg", "WebAgg", "PySide2", "tkinter", "tornado"],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='REACT',
          debug=False,
          strip=False,
          upx=True,
          console=False )