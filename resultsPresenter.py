#!/usr/bin/env python3

__author__ = "Szmiglo"
__version__ = "0.1.0"
__license__ = "MIT"

import os
from config import Config
from db import Db

class ResultsPresenter:
    def __init__(self):
        self.config = Config()
        self.db = Db(False)

    def presentResults(self):
        results = self.db.getDuplicatedDirectories()
        for row in results:
            if str(row[0]).count(",") == 0:
                continue
            os.system('cls' if os.name == 'nt' else 'clear')
            files = str(row[0]).split(",")
            print("Files: %s\n\nDirectory %s (%d occurrences)" % (files, row[1], int(row[2])))
            print("Actions:")
            print("     1. Show duplicated locations")
            print("     2. Ignore directory and proceed")
            inputVal = input()
            if inputVal == "1":
                duplicates = self.db.getDirectoriesWithDuplicatedFiles(row[0])
                self.printDuplicates(duplicates)
                print("\n\nProvide number of row to preserve and rest will be deleted or type 0 to ignore")
                actionVal = input()
                if actionVal == "0":
                    continue
            elif inputVal == "2":
                continue

    def printDuplicates(self, directories):
        print("Found in:")
        i = 1
        for dir in directories:
            print("%d.\t%s" % (i ,dir[0]))
            i += 1