# py-api-clients
:repeat: :snake: simple examples of using public APIs to access data 

**PROVISIONAL SOFTWARE DISCLAIMER**: This software is preliminary and is subject to revision.

## Contents

* [MODAPS](#modaps)
* [EarthExplorer](#earthexplorer)
* [CLASS **not implemented**](#class)

## Installation

All scripts expect to be run in Python2.7, and require some dependencies: 

```bash
pip install -r requirements.txt
```

## MODAPS

* [LAADS Web Service Classic API](https://ladsweb.modaps.eosdis.nasa.gov/tools-and-services/lws-classic/api.php)
* [LAADS Web Service Classic Quick Start Guide](https://ladsweb.modaps.eosdis.nasa.gov/tools-and-services/lws-classic/quick-start.php)

Getting the file locations:
```python
from modaps import API
api = API(debug=False)
urls = api.filesearch('MYD09CMA', 6, '2017/120', datefmt="%Y/%j")
print(urls)  # ['ftp://....2017122031353.hdf']
```

And download them locally:
```python
# Just grab them from the web
urls = [u.replace('ftp', 'https') for u in urls]
print(api.download(urls, loc='./'))  # ['./....2017122031353.hdf']
```

## EarthExplorer

* [EROS Inventory Service JSON API (Machine to Machine)](https://earthexplorer.usgs.gov/inventory/documentation/json-api)

Search for acquisitions:
```python
from earthexplorer import API
api_key = API.login(username='<ers username>')
scenes = API.search(apiKey=api_key, datasetName='LANDSAT_8_C1', maxResults=1)
```

Download scene (**Note: requires special bulk-access approval**)
```python
print(API.download(apiKey=api_key, datasetName='ARD_TILE', products='SR', entityIds=[scenes]))
```

