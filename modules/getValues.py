import sqlite3
from os import path

#Class to get all books or some books for category
class getBooks:

    def __init__(self):
        """ Constructor, connect in database and create cursor """
        self.bookshelf = sqlite3.connect(path.dirname(path.realpath(__file__)) + '/database/bookshelf.db')
        self.cursor = self.bookshelf.cursor()
        
    def getAll(self, table):
        """ Function, get all of bookshelf.db """
        self.cursor.execute(f"SELECT * FROM {table}")
        values = self.cursor.fetchall()
        return values
    
    def getCategory(self, category):
        if int(category) >= 11 or int(category) <= 0:
            return {"code": 400, "msg": "Not exist that category"}
        
        else:
            self.cursor.execute(f"SELECT * FROM books WHERE category = {int(category)}")
            values = self.cursor.fetchall()
            
            if values:
                return {"code": 200, "Values": values[0]}
            
            else:
                return {"code": 200, "msg": "Not found"}
    
    def close(self):
        """Function, close connection with DB"""
        self.bookshelf.close()
