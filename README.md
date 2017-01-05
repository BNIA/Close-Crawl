<div align="center">
  <img src="https://raw.githubusercontent.com/BNIA/Close-Crawl/master/close_crawl/frontend/static/img/logo.png">
</div>
-------------

A tool for scraping public Maryland Judiciary case records through [Case Search](http://www.courts.state.md.us/courts/courtrecords.html). Close Crawl extracts the filing dates, titles, individual addresses and partial costs of case records given a range of case numbers or a precompiled array of case numbers.

## Interface
Close Crawl was initially intended to accompany a non-specified GUI toolkit interface (Tcl/Tk/QT) but later replaced with a Flask web application. The reasons for the new approach included bringing in more lightweight and independent frontend templates and statics and a system independent interface. [gentellela](https://colorlib.com/polygon/gentelella/index.html) was used for the templates.

## Modules
Close Crawl uses Mechanize **(soon to be replaced by [MechanicalSoup](https://github.com/hickford/MechanicalSoup))** to crawl through the records and temporarily download the responses as HTML files. Saving the HTML data locally prevents any loss of progress in case of any network or system disruption during the crawling process, which can be resumed later. The saved files are then parsed using BeautifulSoup, and advanced regular expressions. The data is further cleaned with pandas methods, and the final output is saved as a CSV file.


## Installation

### Production

#### Windows Build
A standalone executable can be found in the `dist` directory. The executable was created on a Windows 10 system, and has been tested against Windows 10 systems, and Windows XP, Windows 7 and Windows 8 virtual environments.

### Development
[![Stories in In Progress](https://badge.waffle.io/BNIA/Close-Crawl.png?label=In%20Progress&title=In%20Progress)](http://waffle.io/BNIA/Close-Crawl)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7780959c71334679ae1996a8060f1390)](https://www.codacy.com/app/sabbir0ahmed0/Close-Crawl?utm_source=github.com&utm_medium=referral&utm_content=BNIA/Close-Crawl&utm_campaign=badger)

If you are not familiar with Python projects on Windows machines, you might want to check out [this quick guide](https://github.com/BNIA/Close-Crawl/blob/dev-sabbir/docs/windows-dev-setup.md).

#### Requirements
- Python 2.7. Python 3 is not supported by Mechanize, the package used for crawling the records, and is therefore not supported. Development for Python 3 support is under way.
- Third party packages listed in `requirements.txt`

Clone the repository, create a virtual environment and install the packages via pip: `pip install -r requirements.txt`.<br>
Or run the Makefile: `make install`

#### Tests
Run the tests: (the tests run on [nose](http://nose.readthedocs.io/en/latest/))
- For UNIX machines, a Makefile has been provided for convenience. Just run: `make test`
- For non-UNIX machines: `nosetests -v -w tests` will work.

#### Executable
[PyInstaller](http://www.pyinstaller.org/) was used to build the Windows executable.
