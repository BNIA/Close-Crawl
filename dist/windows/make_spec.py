#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""env

Makefile helper script to determine if virtualenv is activated"""

if __name__ == '__main__':

	from os import path
	from sys import platform
	from textwrap import dedent

	SPEC_STR = """
		# -*- mode: python -*-

		block_cipher = None

		a = Analysis(['{MOD_PATH}'],
		             pathex=['{PROJ_PATH}'],
		             binaries=None,
		             datas=[('close_crawl\{TEMPLATE_PATH}', '{TEMPLATE_PATH}'),
		             ('close_crawl\{STATIC_PATH}', '{STATIC_PATH}')],
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
		          name='close_crawl',
		          debug=False,
		          strip=False,
		          upx=True,
		          console=True,
		          icon='{ICO_PATH}')
	"""

	BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

	spec_output = dedent(
		SPEC_STR.format(
			MOD_PATH=path.join("close_crawl", "close_crawl.py"),
			PROJ_PATH=BASE_DIR,
			TEMPLATE_PATH=path.join("frontend", "templates"),
			STATIC_PATH=path.join("frontend", "static"),
			ICO_PATH=path.join("frontend", "static", "img", "logo.ico")
		)
	)

	if platform == "win32":
		spec_output = spec_output.replace('\\', "\\\\")

	print(spec_output)
