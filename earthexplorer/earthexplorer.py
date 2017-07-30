import requests, json, os, sys, getpass

class EarthExplorer(object):

    def __init__(self, version='1.4.1'):
        self.baseurl = 'https://earthexplorer.usgs.gov/inventory/json/v/%s/' % version

    def _api(self, endpoint='login', body=None):
        body = {'jsonRequest': json.dumps(body)} if body else {}
        r = requests.post(self.baseurl+endpoint, data=body)
        r.raise_for_status()
        dat = r.json()
        if dat.get('error'):
            sys.stderr.write(': '.join([dat.get('errorCode'), dat.get('error')]))
        return dat

    @classmethod
    def login(cls, username, password=None):
        if password is None:
            password = getpass.getpass('Password (%s): ' % username)
        payload = {'username': username, 'password': password}
        return cls()._api('login', payload).get('data')

    @classmethod
    def search(cls, **kwargs):
        return cls()._api('search', kwargs).get('data')

    @classmethod
    def download(cls, **kwargs):
        return cls()._api('download', kwargs).get('data')

