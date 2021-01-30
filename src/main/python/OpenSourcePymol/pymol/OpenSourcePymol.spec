# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['__init__.py', '../pmg_qt/TextEditor.py', '../pmg_qt/pymol_qt_gui.py', '../pmg_qt/properties_dialog.py', '../pmg_qt/get_files.py', '../pmg_qt/__init__.py',
            '../pmg_qt/mimic_tk.py', '../pmg_qt/pymol_gl_widget.py', '../pmg_qt/advanced_settings_gui.py', '../pmg_qt/volume.py', '../pmg_qt/builder.py', '../pmg_qt/mimic_pmg_tk.py',
            '../pmg_qt/file_dialogs.py', '../pmg_qt/keymapping.py',
            '../pmg_tk/TextEditor.py', '../pmg_tk/get_files.py', '../pmg_tk/__init__.py', '../pmg_tk/Setting.py', '../pmg_tk/PyMOLMapLoad.py', '../pmg_tk/volume.py', '../pmg_tk/PMGApp.py',
             '../pmg_tk/Demo.py', '../pmg_tk/SetEditor.py', '../pmg_tk/ColorEditor.py',
             '../pmg_qt/syntax/pml.py', '../pmg_qt/syntax/pmlparser.py', '../pmg_qt/syntax/python.py'],
             pathex=['/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol',
             '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/',
             '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt/',
             '/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt/syntax/'],
             binaries=[('/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/_cmd.cpython-39-darwin.so','.')],
             datas=[("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/pymol_path/*", "pymol/pymol_path"),
                    ("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pymol/pymol_path/data/*", "pymol/pymol_path/data"),
                    ("/Users/gvi022/Onedrive - UiT Office 365/programming/pymol/test/lib/python3.9/site-packages/pmg_qt/forms/*", "pymol/pmq_qt/forms")],
             hiddenimports=['pymol.callback', 'pymol.controlling', 'pymol.internal', 'pymol.vfont', 'pymol.cmd', 'pymol.morphing', 'pymol.moving', 'pymol._gui',
                            'pymol.parsing', 'pymol.editing', 'pymol.importing', 'pymol.diagnosing', 'pymol.util', 'pymol.monitoring', 'pymol.externing',
                            'pymol.keywords', 'pymol.constants', 'pymol.selector', 'pymol.headering', 'pymol.selecting', 'pymol.preset', 'pymol.constants_palette',
                            'pymol.setting', 'pymol.experimenting', 'pymol.checking', 'pymol.colorramping', 'pymol.commanding', 'pymol.cgo', 'pymol.parser', 'pymol.api',
                            'pymol.exporting', 'pymol.menu', 'pymol.wizarding', 'pymol.rpc', 'pymol.pymolhttpd', 'pymol.creating', 'pymol.completing', 'pymol.locking',
                            'pymol.helping', 'pymol.feedingback', 'pymol.colorprinting', 'pymol.movie', 'pymol.fitting', 'pymol.invocation', 'pymol.xwin', 'pymol.editor',
                            'pymol.xray', 'pymol.lazyio', 'pymol.shortcut', 'pymol.computing', 'pymol.gui', 'pymol.seqalign', 'pymol.viewing', 'pymol.povray',
                            'pymol.mpeg_encode', 'pymol.querying', 'pymol.keyboard', 'Qt',
                            'pmg_qt', 'pmg_tk'],
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
         bundle_identifier=None,
         info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'OpenSourcePymol',
                    'CFBundleTypeRole': 'Viewer', 
                    'CFBundleTypeIconFile': 'openSourcePymol.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'LSHandlerRank': 'Alternate'
                    }
                ]
            },
         )
