# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run_pymol.py'],
             pathex=['/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages'],
             binaries=[('pymol/_cmd.cpython-39-darwin.so', 'pymol')],
             datas=[("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/pymol_path/*","pymol/pymol_path/data")
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
