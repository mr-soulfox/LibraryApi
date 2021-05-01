import sqlite3
from os import path

#Class to add and create table
class Database:
    
    def __init__(self):
        """ Constructor, connect in database and create cursor """
        self.bookshelf = sqlite3.connect(path.dirname(path.realpath(__file__)) + '/database/bookshelf.db')
        self.cursor = self.bookshelf.cursor()
    
    def verifyTableExist(self, table):
        """ Function, verify if a table exist in bookshelf.db """
        try:
            self.cursor.execute(f"CREATE TABLE {table} (title text, category integer, publisher text, linkImg text, authors text, link text)")
            
            #Did not exist
            return True
        
        except:
            #Exist
            return True
    
    def valueExist(self, values):
        """ Function, verify if value exist in DB (bookshelf.db) """
        try:
            self.cursor.execute(f"SELECT COUNT(1) FROM books WHERE title = '{values['title']}'")
            count = self.cursor.fetchall()
            
        except sqlite3.Error as error:
            return "error"
        
        if int(count[0][0]) >= 1:
            return True
        
        else:
            return False

    def addBook(self, bookValues):
        """ Function, add values in bookshelf.db """
        if type(bookValues) == dict:
            tableExist = self.verifyTableExist('books')
            
            if tableExist:
                #add values in table books
                try:                   
                    
                    #Grouping the values
                    authors = ",".join(bookValues['authors'])
                     
                    self.cursor.execute(f"INSERT INTO books VALUES ('{bookValues['title']}', '{bookValues['category']}', '{bookValues['publisher']}', '{bookValues['linkImg']}', '{authors}', '{bookValues['link']}')")
                    
                except sqlite3.Error as error:
                    return {"code":400, "msg":f"{error}"}
                
                self.bookshelf.commit()
                return {"code":201, "msg":"created with sucess"}
                
            else:
                return {"code":500, "msg":"internal error"}
            
        else:
            #erro, type bookValues incorrect
            return {"code":400, "msg":"Error: type incorrect"}
    
    def close(self):
        """Function, close connection with DB"""
        self.bookshelf.close()
        
