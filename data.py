import json

class DataWrapper:
    data = None

    def __init__(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)

    def get(self, var):
        return self.data[var]
