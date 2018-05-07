# -*- mode: python -*-

block_cipher = None


added_files = [
         ( 'assets', 'assets' )]
a = Analysis(['__init__.py'],
             pathex=['C:\\python36\\jeu_python'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
			 
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
		
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Mad Runner 1.0',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
		  icon="C:\\python36\\jeu_python\\assets\\img\\icon\\propicon48.ico",
          console=False,
		  version="C:\\python36\\jeu_python\\version.rc")