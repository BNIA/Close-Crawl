# Development on Windows
This guide is for Windows users looking to install the dependancies required for setting up a Python project. Instructions were derived from this [article](http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/).

## Requirements
- [Python (>2.7)](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)

### Get Python and pip
Download and install the latest version of [Python 2.7](https://www.python.org/downloads/). In the installer, make sure to check the options for pip and to add C:\Python27\ to the path. Once installed, open up a Powershell and enter the command `python`. If the installation successfully added Python to the path, the following should appear:

Then enter the command `pip`. If installation was successful, the following should appear:

If the command fails, then download the pip script manually with [get-pip.py](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py). Run `python get-pip.py`


### Get virtualenv
Once both Python and its package manager pip have been installed, run the following commands to install virtualenv for Powershell:<br>
```
pip install virtualenv
pip install virtualenvwrapper-powershell
```

## Setup

### Download the repository
If you have git, run `git clone https://github.com/BNIA/Close-Crawl.git`. If not, just download and extract the [repository](https://github.com/BNIA/Close-Crawl).

### Set up the development environment
Navigate to the project on your terminal, then initialize a virtual environment: `virtualenv <ENV_NAME>`. Once the virtual environment is initialized, activate it by running: `.\<ENV_NAME>\Scripts\activate`. Lastly, download all the required packages through pip: `pip install -r requirements.txt`
