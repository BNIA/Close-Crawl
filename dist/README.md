# Production

A single Windows executable file is compiled as the final product.

## Build

[PyInstaller](http://www.pyinstaller.org/) was used to build the Windows executable. The spec file is used for the configuration of the build.

To build, run `pyinstaller close_crawl.spec`

## System dependancies

The Windows executable was built in a win32 environment on Windows 10, and has been tested against Windows 10 systems, and Windows XP, Windows 7 and Windows 8 virtual environments. Linux executables were also created and tested against during development.
