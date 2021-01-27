# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['REACT.py'],
             pathex=['/Users/gvi022/Onedrive - UiT Office 365/programming/REACT/src/main/python'],
             binaries=[('/Users/gvi022/Onedrive - UiT Office 365/programming/REACT/src/main/python/openPymol/pymol/_cmd.cpython-39-darwin.so', 'openPymol/pymol')],
             datas=[],
             hiddenimports=[],
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
          [],
          name='REACT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
