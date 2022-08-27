import flask
from flask import request,jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Hardcoded test value
# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=["GET"])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>",404


# To find specific resource
@app.route('/api/v1/resources/books', methods=['GET'])
# With DB implementation
def api_filter():
    query_params = request.args
    # id = query_params.get("id")
    published = query_params.get("published")
    author = query_params.get("author")
    query = "SELECT * FROM books WHERE"

    to_filter = []

    # if id:
    #     query += " id=? AND "
    #     to_filter.append(id)
    if published:
        query += " published=? AND "
        to_filter.append(published)
    if author:
        query += "author=?"
        to_filter.append(author)
    if not (published or author):
        return page_not_found(404)
    
    query = query + ";"
    # print(query)
    conn = sqlite3.connect("books.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)

# Below implementation is for : Without DB 
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     # print("args :", request.args)
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error"

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)
#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)
app.run()

