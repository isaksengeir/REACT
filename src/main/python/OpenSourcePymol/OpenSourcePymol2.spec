# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run_pymol.py'],
             pathex=['/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/Qt',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/plugins',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/wizard',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/stereochemistry',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt/syntax',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt/forms'
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol2',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_tk',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_tk/skins',
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_tk/startup'
                     '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol'
                     ],
             binaries=[('pymol/_cmd.cpython-39-darwin.so', 'pymol')],
             datas=[("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/pymol_path/*","pymol/pymol_path/data"),
                    ("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt*", "pmg_qt"),
                    ("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt/forms/*", "pmg_qt/forms"),
                    ("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/pymol_path/LICENSE", "pymol/pymol_path"),
                    ("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/plugins/*", "pymol/plugins")],
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
          [],
          exclude_binaries=True,
          name='OpenSourcePymol',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='OpenSourcePymol')
app = BUNDLE(coll,
         name='OpenSourcePymol.app',
         icon="openSourcePymol.icns",
         bundle_identifier='com.opensourcepymol',
          info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'My File Format',
                    'CFBundleTypeIconFile': 'openSourcePymol.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'CFBundleTypeRole' : 'Editor',
                    'LSHandlerRank': 'Owner'
                    }
                ]
            },
         )
