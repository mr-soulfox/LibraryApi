import sqlite3
from os import path

#Class to delete value by title
class delete:

    def __init__(self):
        """ Constructor, connect in database and create cursor """
        self.bookshelf = sqlite3.connect(path.dirname(path.realpath(__file__)) + '/database/bookshelf.db')
        self.cursor = self.bookshelf.cursor()
    
    def valueExist(self, title):
        """ Function, verify if value exist in DB (bookshelf.db) """
        try:
            self.cursor.execute(f"SELECT COUNT(1) FROM books WHERE title = '{title}'")
            count = self.cursor.fetchall()
            
        except sqlite3.Error as error:
            return "error"
        
        if int(count[0][0]) >= 1:
            return True
        
        else:
            return False
        
    def delete(self, title):
        """ Function, delete register from DB """
        exist = self.valueExist(title)
        
        if exist == "error":
            return {"code":500, "msg": "Internal error"}
        
        elif exist:
            try:
                self.cursor.execute(f"DELETE FROM books WHERE title = '{title}'")
                self.bookshelf.commit()
                
                return {"code": 200, "msg": "Deleted with success"}
            
            except sqlite3.Error as error:
                return {"code": 400, "msg": error}
        
        else:
            return {"code": 200, "msg": "Value not found"}
    
    def close(self):
        """Function, close connection with DB"""
        self.bookshelf.close()
