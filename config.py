#!/usr/bin/env python3

__author__ = "Szmiglo"
__version__ = "0.1.0"
__license__ = "MIT"

import json

class Config:
    def __init__(self):
        with open('config.json') as json_file:
            self._config = json.load(json_file)
    
    def getValue(self, key):
        return self._config[key]