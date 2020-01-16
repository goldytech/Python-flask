import json

from flask import Flask, jsonify, request, Response
from book_model import *

from settings import *



@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    if return_value is None:
        invalid_book_object_error_msg = {
            "error": f"Book with ISBN number {isbn} not found."
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
        return response
    else:
        # return return_value.__repr__()
        response = Response(json.dumps(return_value), status=200, mimetype='application/json')
        return response


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
        Book.add_book(new_book['name'], new_book['price'], new_book["isbn"])
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
    Book.replace_book(new_book['isbn'], new_book['name'], new_book['price'])
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

    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])

    if "name" in request_data:
        Book.update_book_name(request_data['name'])

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    book_to_be_deleted = Book.get_book(isbn)
    if book_to_be_deleted is None:
        invalid_book_object_error_msg = {
            "error": "Book with ISBN number provided not found, so unable to delete.",
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
        return response
    else:
        Book.delete_book(book_to_be_deleted['isbn'])
        response = Response("", status=204)
        return response
