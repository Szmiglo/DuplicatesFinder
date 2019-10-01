import sqlite3
import json
import os
from config import Config

class Db:
    def __init__(self, removeDb = True):
        self.config = Config()
        if removeDb == True:
            try:
                os.remove("./files.db")
            except PermissionError:
                print("Looks like files.db is currently in use. Please release the resource and try again.")
                os._exit(1)
        self.conn = sqlite3.connect('./files.db')
        self.cursor = self.conn.cursor()
        self.ensureSchemaCreated()
    
    def __del__(self):
        self.conn.close()

    def ensureSchemaCreated(self):
        self.cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='files';''')
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute('''CREATE TABLE files
             ([id] INTEGER PRIMARY KEY,[fileName] text,[extension] text, [filePath] text, [fileSize] integer, [fileHash] text, [createdDate] date, [modifiedDate] date)''')

    def insertFile(self, name, extension, path, size, hash, createdDate, modifiedDate):
        dataTuple = (name, extension, path, size, hash, createdDate, modifiedDate)
        self.cursor.execute(''' INSERT INTO files (fileName, extension, filePath, fileSize, fileHash, createdDate, modifiedDate) values (?, ?, ?, ?, ?, ?, ?)''', dataTuple)
        self.conn.commit()

    def getDuplicatedDirectories(self):
        self.cursor.execute('''SELECT 
                filesList, filePath,
                COUNT(*) occurrences
            FROM (select group_concat(fileName) as filesList, filePath
            from files
            group BY
                filePath)
            GROUP BY
                filesList
            HAVING 
                COUNT(*) > 1
            order by occurrences desc
            ''')
        return self.cursor.fetchall()
    
    def getDirectoriesWithDuplicatedFiles(self, filesList):
        self.cursor.execute('''select filePath from   
            (select group_concat(fileName) as filesList, filePath
            from files
            group BY
                filePath)
                
            where filesList = ? ''', (filesList, ))
        return self.cursor.fetchall()

