<div align="center">
  <img src="https://raw.githubusercontent.com/BNIA/Close-Crawl/master/close_crawl/frontend/static/logo.png">
</div>
-------------

A tool for scraping public Maryland Judiciary case records through [Case Search](http://www.courts.state.md.us/courts/courtrecords.html). Close Crawl extracts the filing dates, titles, individual addresses and partial costs of case records given a range of case numbers or a precompiled array of case numbers.


## Installation

### Windows Build
A standalone executable can be found in the `dist` directory. The executable was created on a Windows 10 system, and has been tested against Windows 10 systems, and Windows XP, Windows 7 and Windows 8 virtual environments.

### Development
[![Stories in In Progress](https://badge.waffle.io/BNIA/Close-Crawl.png?label=In%20Progress&title=In%20Progress)](http://waffle.io/BNIA/Close-Crawl)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7780959c71334679ae1996a8060f1390)](https://www.codacy.com/app/sabbir0ahmed0/Close-Crawl?utm_source=github.com&utm_medium=referral&utm_content=BNIA/Close-Crawl&utm_campaign=badger)


## Abstract

### Interface
Close Crawl was initially intended to accompany a non-specified GUI toolkit interface (Tcl/Tk/QT) but later replaced with a Flask web application. The reasons for the new approach included bringing in more lightweight and independent frontend templates and statics and a system independent interface.

### Modules
Close Crawl uses Mechanize (soon to be replaced by MechanicalSoup) to crawl through the records and temporarily download the responses as HTML files. Saving the HTML data locally prevents any loss of progress in case of any network or system disruption during the crawling process, which can be resumed later. The saved files are then parsed using BeautifulSoup, and advanced regular expressions. The data is further cleaned with pandas methods, and the final output is saved as a CSV file.
