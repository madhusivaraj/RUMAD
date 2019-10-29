# - Installing and understanding what it does
# - Build GET and POST /books route with insert and find
# - you'll have to explain the JSON encoder.

import json
from flask import Flask, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
book_db = client['book_db']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#insert_book
@app.route("/books", methods=["POST", "GET"])
def books():
    if request.method == "GET":
        book_collection = book_db['books']
        return JSONEncoder().encode(list(book_collection.find()))
    elif request.method == "POST":
        body = request.get_json()
        title = body["title"]
        book = {
            "title": title,
            "author": body["author"],
            "description": body["description"]
        }
        book_collection = book_db['books']
        if book_collection.count({'title': title}, limit=1):
            return "Book already inserted"
        book_collection.insert_one(book)
        return "Book inserted"


#search_book
@app.route("/books/<book_title>", methods=["GET"])
def find_book(book_title):
    book_collection = book_db['books']
    if book_collection.count({'title': book_title}, limit=1):
        return JSONEncoder().encode(book_collection.find_one({"title": book_title}))
    else:
        return "Book not found"

