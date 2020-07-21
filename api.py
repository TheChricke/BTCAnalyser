import requests


class ApiFetcher:
    baseurl = ""
    path = ""
    parameters = {}

    def __init__(self, baseUrl, path, parameters):
        self.baseurl = baseUrl
        self.path = path
        self.parameters = parameters

    def fetchData(self):
        r = requests.get(self.baseurl + self.path, self.parameters)
        return r.json()
