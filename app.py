import json

from flask import Flask, jsonify, request, Response

app = Flask(__name__)

books = [
    {
        'name': 'A',
        'price': 7.99,
        'isbn': 9780394800165
    },
    {
        'name': 'B',
        'price': 6.99,
        'isbn': 9792371000193
    },
    {
        'name': 'C',
        'price': 7.99,
        'isbn': 9800394800165
    },
    {
        'name': 'D',
        'price': 6.99,
        'isbn': 9812371000193
    },
    {
        'name': 'E',
        'price': 7.99,
        'isbn': 9820394800165
    },
    {
        'name': 'F',
        'price': 6.99,
        'isbn': 9832371000193
    },
    {
        'name': 'G',
        'price': 7.99,
        'isbn': 9840394800165
    },
    {
        'name': 'H',
        'price': 6.99,
        'isbn': 9852371000193
    },
    {
        'name': 'I',
        'price': 7.99,
        'isbn': 9860394800165
    },
    {
        'name': 'K',
        'price': 6.99,
        'isbn': 9872371000193
    },
    {
        'name': 'L',
        'price': 7.99,
        'isbn': 9880394800165
    },
    {
        'name': 'M',
        'price': 6.99,
        'isbn': 9892371000193
    },
    {
        'name': 'N',
        'price': 7.99,
        'isbn': 9900394800165
    },
    {
        'name': 'O',
        'price': 6.99,
        'isbn': 9912371000193
    },
    {
        'name': 'P',
        'price': 7.99,
        'isbn': 9920394800165
    },
    {
        'name': 'Q',
        'price': 6.99,
        'isbn': 9932371000193
    },
    {
        'name': 'R',
        'price': 7.99,
        'isbn': 9940394800165
    },
    {
        'name': 'S',
        'price': 6.99,
        'isbn': 9952371000193
    }
]


@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)


def valid_book_object(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = f"/books/{str(new_book['isbn'])}"
        return response
    else:
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response


def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


# PUT /books/{isbn}
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        current_isbn = book["isbn"]
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


def valid_patch_request_data(request_data):
    if "name" in request_data or "price" in request_data:
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if not valid_patch_request_data(request_data):
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response
    updated_book = {}
    if "price" in request_data:
        updated_book["price"] = request_data['price']
    if "name" in request_data:
        updated_book["name"] = request_data['name']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0;
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalid_book_object_error_msg = {
        "error": "Book with ISBN number provided not found, so unable to delete.",
    }
    response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
    return response
