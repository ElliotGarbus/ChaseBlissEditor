# -*- mode: python -*-

import os

spec_root = os.path.abspath(SPECPATH)
block_cipher = None
app_name = 'ChaseBlissEditor'
mac_icon = ''


a = Analysis(['../main.py'],
             pathex=[spec_root],
             binaries=[],
             datas=[('../*.kv', '.'), ('../*.png', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
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
          name=app_name,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name=app_name)

app = BUNDLE(coll,
             name=app_name + '.app',
             icon=mac_icon,
             bundle_identifier=None)
