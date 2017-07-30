import os
import datetime

from SOAPpy import SOAPProxy
import requests


WEBSRV_URL = 'https://modwebsrv.modaps.eosdis.nasa.gov/axis2/services/MODAPSservices'

class MODAPS(object):
    def __init__(self, debug=False):
        self.url = WEBSRV_URL
        self.client = SOAPProxy(self.url)
        if debug:
            self.client.config.debug = 1

    def search(self, product, collection, datestr, datefmt='%Y%m%d',
               north=90, south=-90, east=180, west=-180, coords="coords",
               daynight="DNB"):
        """ Performs a spatio-temporal search against the API
        :param product: Product name (or names, comma-delimited)
        :param collection: Archive Collection          [ int ]
        :param datestr: Date to search (only searches 1 day)
        :param datefmt: Date parse expression
        :param north: North boundary of spatial window [float]
        :param south: South boundary of spatial window [float]
        :param east: East boundary of spatial window   [float]
        :param west: West boundary of spatial window   [float]
        :param coords: Whether spatial window is specified in coords or tiles
        :param daynight: day (D), night (N), or both (B) acquisitions
        """
        parser = lambda x: datetime.datetime.strptime(x, datefmt)
        startstr = parser(datestr).strftime('%Y-%m-%d 00:00:00')
        endstr = parser(datestr).strftime('%Y-%m-%d 23:59:59')
        request = dict(product=product, collection=collection,
                       startTime=startstr, endTime=endstr,
                       north=north, south=south, east=east, west=west,
                       coordsOrTiles=coords, dayNightBoth=daynight)
        response = self.client.searchForFiles(**request)
        return response

    def fileurls(self, fileids):
        """ Find the datafiles on the FTP server
        :param fileids: The file IDS of the data files
        """
        if isinstance(fileids, list):
            fileids = ','.join(fileids)
        request = dict(fileIds=fileids)
        response = self.client.getFileUrls(**request)
        if not isinstance(response, list):
            response = [response]
        return response

    def filesearch(self, product, collection, datestr, datefmt='%Y%m%d'):
        """ Performs a global search and returns the FTP urls
        :param product: Product name (or names, comma-delimited)
        :param collection: Archive Collection
        :param datestr: Date to search (only searches 1 day)
        :param datefmt: Date parse expression
        """
        fids = self.search(product, collection, datestr, datefmt)
        urls = self.fileurls(fids)
        return urls

    @staticmethod
    def download(urls, loc='./'):
        """ Stream URLs into local filenames
        :param urls: Full URL path to HTTP filenames
        :param loc: Local directory to save output files
        """
        downloaded = list()
        for url in urls:
            local = os.path.join(loc, url.split('/')[-1])
            r = requests.get(url, stream=True)
            with open(local, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            downloaded.append(local)
        return downloaded

