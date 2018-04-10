# -*- mode: python -*-

# Commande: pyinstaller --clean --onefile __init__.spec

block_cipher = None

added_files = [
         ( 'config', 'config' ),
         ( 'assets', 'assets' )]
a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\€¤\\PycharmProjects\\MadRunner\\jeu_python'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
			 
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
		
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='__init__',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
