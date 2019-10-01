#!/usr/bin/env python3

__author__ = "Szmiglo"
__version__ = "0.1.0"
__license__ = "MIT"

import os, sys, time
import os.path
import hashlib
import configparser
from db import Db
from config import Config
from resultsPresenter import ResultsPresenter
from time import perf_counter 

class DuplicatesFinder: 
    def __init__(self):
        self.db = Db()
        self.config = Config()

    def findDuplicates(self, directories):
        start = perf_counter()  
        for directory in directories:
            if not os.path.exists(directory):
                print("Given directory %s doesn't exist!" % directory)
                continue
            self.traverseDirectory(directory)
        print("Elapsed time in seconds:", perf_counter()-start) 
        print("Traversing directories finished. Now selecting duplicates")

    def traverseDirectory(self, parentDir):
        for dirName, subdirs, fileList in os.walk(parentDir):
            print('Scanning %s...' % dirName)
            [subdirs.remove(d) for d in list(subdirs) if d in self.getExcludedDirs()]
            if self.shouldIgnoreDirectory(dirName):
                print("Ignoring directory %s" % dirName)
                continue
            for filename in fileList:
                # Get the path to the file
                path = os.path.join(dirName, filename)
                # Calculate hash
                if self.config.getValue("omit_calculating_hash"):
                    hash = ""
                else:
                    hash = self.hashfile(path)

                modifiedDate = time.ctime(os.path.getmtime(path))
                createdDate = time.ctime(os.path.getctime(path))
                size = os.path.getsize(path)
                extension = os.path.splitext(path)[1]
                if size <= int(self.config.getValue("ignore_files_below_size")):
                    continue
                self.db.insertFile(filename, extension, dirName, size, hash, createdDate, modifiedDate)   
    
    def getExcludedDirs(self):
        return self.config.getValue("ignore_dirs")

    def shouldIgnoreDirectory(self, dirPath):
        return os.path.basename(dirPath) in self.config.getValue("ignore_dirs")

    # Joins two dictionaries
    def joinDicts(self, dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] = dict1[key] + dict2[key]
            else:
                dict1[key] = dict2[key]
    
    
    def hashfile(self, path, blocksize = 65536):
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()
    
    def printResults(self, dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            print('Duplicates Found:')
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________')
            for result in results:
                for subresult in result:
                    print('\t\t%s' % subresult)
                print('___________________')
    
        else:
            print('No duplicate files found.')
 
 
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print("DuplicatesFinder v%s" % __version__)
    print("Choose your action:")
    print("     1. Scan for duplicates")
    print("     2. Show results of previous run")
    action = int(input())
    if action == 1:
        print("Type directories to be searched separated by comma:")
        directoriesList = input()
        finder = DuplicatesFinder()
        finder.findDuplicates(directoriesList.split(","))
    elif action == 2:
        presenter = ResultsPresenter()
        presenter.presentResults()
    else:
        print("Incorrect option")