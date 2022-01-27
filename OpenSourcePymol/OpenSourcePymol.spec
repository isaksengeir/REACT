# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None
file_path = os.getcwd()

a = Analysis(['run_pymol.py'],
             pathex=[f'file_path'],
             binaries=[('pymol/_cmd.cpython-39-darwin.so', 'pymol')],
             datas=[(f"{file_path}/pymol/pymol_path/*","pymol/pymol_path/data")
                    ],
             hiddenimports=['pymol','pymol.povray', 'pymol.parser'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          icon="openSourcePymol.icns",
          strip=False,
          upx=True,
          name='OpenSourcePymol',
          debug=False,
          console=False )
