# -*- mode: python -*-

# Commande: pyinstaller --clean --onefile __init__.spec

block_cipher = None

added_files = [
         ( '..\\LICENSE', '' ),
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
          name='Mad Runner 1.0',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
		  icon='C:\\Users\\€¤\\PycharmProjects\\MadRunner\\jeu_python\\assets\\img\\icon\\propicon48.ico',
          console=False,
		  version='version.rc'
)