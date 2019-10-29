# {
# 	"title": "Little Women5",
# 	"author": "Louisa May Alcott5",
# 	"description": "4 sisters in MA5"
# }

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
@app.route("/books", methods=["POST"])
def books():
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
@app.route("/books", methods=["GET"])
def find_book():
    title = request.args.get('title')
    book_collection = book_db['books']
    if title is None:
        return JSONEncoder().encode(list(book_collection.find()))
    elif book_collection.find_one({'title': title}):
        return JSONEncoder().encode(book_collection.find_one({"title": title}))
    else:
        return "Book not found"
