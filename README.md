# pyAMT 
[![PyPI version](https://badge.fury.io/py/pyAMT.svg)](https://badge.fury.io/py/pyAMT) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


An unofficial python API wrapper for [AMT's](https://www.amt.genova.it/) (public transportation for my city) undocumented API. Endpoints were obtained examining the [official android application](https://play.google.com/store/apps/details?id=it.genova.amt.app), I am not in any way affiliated with [AMT](https://www.amt.genova.it/).

## Installation

Install with `pip3 install pyAMT`

## Usage
```py
from pyAMT import AMT

amt = AMT()

# get next departures from a stop
amt.departures("0360")

# get information about a line stop
amt.stop("0395")

#get information about a line
amt.line("15")

# add "_1" for Start->End and "_2" for End->Start
amt.lineStops("015-00_1")

# get detailed information about a line (including timetables)
amt.linesDetailedInfo("15","13","03","2022")
```


Build for [test.pypi.org](https://test.pypi.org/simple/):
```
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```
Install test:
```
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyAMT
```