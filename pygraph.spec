# -*- mode: python -*-

block_cipher = None


a = Analysis(['pygraph.py'],
             pathex=['dlls', 'D:\\git\\DeepLearning\\pygraph'],
             binaries=[],
             datas=[],
             hiddenimports=['tkinter', 'scipy', 'matplotlib'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pygraph',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
