# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['REACT.py'],
             pathex=['/Users/gvi022/programming/REACT/'],
             binaries=[],
             datas=[("/Users/gvi022/programming/REACT/OpenSourcePymol/dist/OpenSourcePymol.app/", "OpenSourcePymol/dist/OpenSourcePymol.app/")],
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
          [],
          exclude_binaries=True,
          name='REACT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='REACT')
app = BUNDLE(coll,
         name='REACT.app',
         icon="REACT_256.icns",
         bundle_identifier='com.REACT',
          info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'My File Format',
                    'CFBundleTypeIconFile': 'REACT_256.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'CFBundleTypeRole' : 'Editor',
                    'LSHandlerRank': 'Owner'
                    }
                ]
            },
         )
