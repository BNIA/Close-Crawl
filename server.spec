# -*- mode: python -*-

block_cipher = None


a = Analysis(['close_crawl/server.py'],
             pathex=['/home/sabbir/Desktop/close-crawl'],
             binaries=None,
             datas=[('close_crawl/frontend/templates', 'frontend/templates'),
             ('close_crawl/frontend/static', 'frontend/static')],
             hiddenimports=[],
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
          name='server',
          debug=False,
          strip=False,
          upx=True,
          console=True )
