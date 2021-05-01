import sqlite3
from os import path

#Class to update book for id
class updateBook:
    
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
        
    def update(self, title, edit, newValue):
        """ Function, update some info in bookshelf.db """
        exist = self.valueExist(title)
        
        if exist == "error":
            return {"code": 500, "msg": "Internal error"}
        
        elif exist:
            try:
                if edit != 'category':
                    self.cursor.execute(f"UPDATE books SET {edit} = '{newValue}' WHERE title = '{title}'")
                    self.bookshelf.commit()
                    
                    return {"code":200, "msg":"Update successfully", "value": f"{newValue} in {edit}"}
                
                elif edit == 'category' and type(newValue) == int:
                    self.cursor.execute(f"UPDATE books SET {edit} = {int(newValue)} WHERE title = '{title}'")
                    self.bookshelf.commit()                    
                    
                    return {"code":200, "msg":"Update successfully", "value": f"{newValue} in {edit}"}
                
                else:
                    return {"code": 500, "msg": "Internal error"}
                
            except sqlite3.Error as error:
                return {"code": 400, "msg": f"{error}"}
            
        else:
            return {"code": 200, "msg": "Value not exist"}
                
    
    def close(self):
        """Function, close connection with DB"""
        self.bookshelf.close()