from flask import Flask, jsonify, request, render_template
from modules import bookshelf, getValues, updateValues, deleteValues

app = Flask(__name__)

#API page
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


#Add books on sqlite database
@app.route('/obras', methods=['POST'])
def addBooks():
    """ Router, add values in database """
    book = dict(request.json)
    
    #Create connection and instance database class
    database = bookshelf.Database()
    exist = database.valueExist(book)
    
    #conditional to verify if value exist on table
    if exist == "error":
        return jsonify({"msg": {"code":500, "msg": "internal error"}})
    
    elif not exist:
        msg = database.addBook(book)
        database.close()
        
    else:
        database.close()
        return jsonify({"msg": {"code": 400, "msg": "value exist on table", "exist": True}})
    
    return jsonify({"msg": msg})


#Get books to category or name
@app.route('/obras/<string:cat>', methods=['GET'])
def getBooks(cat):
    #Create connection and instance getBooks class
    get = getValues.getBooks()
    
    if cat == 'all':
        values = get.getAll('books')
        get.close()
        return jsonify({"code": 200, "msg": "Get sucess", "select": cat, "values": values})

    elif cat.isnumeric():
        values = get.getCategory(cat)
        get.close()
        return jsonify(values)
    
    else:
        return jsonify({"code": 400, "msg": "Invalid url parameter", "select": cat})


#Update book details
@app.route('/obras/<string:title>', methods=['PUT'])
def update(title):
    #Create connection and instance getBooks class
    update = updateValues.updateBook()
    
    #get values in json
    values = dict(request.json)
    
    if bool(values['edit']) and bool(values['newValue']):
        msg = update.update(title, values['edit'], values['newValue'])
        update.close()
        return jsonify(msg)
    
    else:
        return jsonify({"code": 400, "msg": "Invalid request", "values": values})


#Delete book
@app.route('/obras/<string:title>', methods=['DELETE'])
def delete(title):
    #Create connection and instance getBooks class
    delValues = deleteValues.delete()
    
    if bool(title):
        msg = delValues.delete(title)
        delValues.close()
        return jsonify(msg)
    
    else:
        return jsonify({"code": 400, "msg": "Invalid title"})

#run with debug
app.run(debug=True)
