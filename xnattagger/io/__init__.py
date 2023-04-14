from pathlib import Path
import urllib
import requests

def get(uri):
    parts = urllib.parse.urlparse(uri)
    if not parts.scheme or parts.scheme == 'file':
        uri = f'{parts.netloc}{parts.path}'
        uri = Path(uri).absolute()
        uri = f'file://{uri}'
    session = requests.session()
    session.mount('file://', LocalFileAdapter())
    r = session.get(uri)
    r.raise_for_status()
    return r.content

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):
        resp = requests.Response()
        resp.raw = open(request.path_url, 'rb')
        resp.status_code = 200
        return resp
