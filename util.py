import requests
from urllib.parse import urlparse

def requestData(method = "PROPFIND", hostname = "", depth = 0, data = "", auth = ("","")):
    response = requests.request(
        method,
        hostname,
        data = data, 
        headers = {
            "Depth" : str(depth)
        },
        auth = auth 
    )

    if response.status_code<200 or response.status_code>299:
        raise Exception('http code error' + ret.status_code)

    return response

def getHostnameFromUrl(url):
    parsedUrl = urlparse(url)
    hostname = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUrl)
    return hostname
