from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Configure the database (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123%21%40%23qweQWE@localhost/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Corrected key name
db = SQLAlchemy(app)

# Define the Member model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    joined_date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)

# Initialize the database and create tables
with app.app_context():
    db.create_all()

# Error handling for 404 (Not Found)
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

# Error handling for 500 (Internal Server Error)
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback any pending changes in case of an error
    return jsonify({"error": "Internal server error"}), 500

# Routes for adding new Members
@app.route('/library/members', methods=['POST'])
def add_member():
    try:
        data = request.json
        member = Member(name=data['name'], email=data['email'])
        db.session.add(member)
        db.session.commit()
        return jsonify({"success": True, "member": {"id": member.id, "name": member.name, "email": member.email}}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route for fetching all members
@app.route('/library/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{"id": m.id, "name": m.name, "email": m.email, "joined_date": m.joined_date} for m in members])

# Route for fetching a specific member by id
@app.route('/library/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)  # Automatically raises 404 if member not found
    return jsonify({"id": member.id, "name": member.name, "email": member.email, "joined_date": member.joined_date})

# Route for updating existing member
@app.route('/library/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        data = request.json
        member = Member.query.get_or_404(id)
        member.name = data.get('name', member.name)
        member.email = data.get('email', member.email)
        db.session.commit()
        return jsonify({"success": True, "member": {"id": member.id, "name": member.name, "email": member.email}})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route for deleting a member
@app.route('/library/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        member = Member.query.get_or_404(id)
        db.session.delete(member)
        db.session.commit()
        return jsonify({"success": True, "message": "Member deleted"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Routes for adding a new Book
@app.route('/library/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        book = Book(id=data['id'], title=data['title'], author=data['author'], available=data["available"])
        db.session.add(book)
        db.session.commit()
        return jsonify({"success": True, "book": {"id": book.id, "title": book.title, "author": book.author, "available": book.available}}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Routes for getting all books
@app.route('/library/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books])

# Routes for getting specific book by id
@app.route('/library/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)  # Automatically raises 404 if book not found
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "available": book.available})

# Routes for updating book details
@app.route('/library/books/<int:id>', methods=['PUT'])
def update_book(id):
    try:
        data = request.json
        book = Book.query.get_or_404(id)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.available = data.get('available', book.available)
        db.session.commit()
        return jsonify({"success": True, "book": {"id": book.id, "title": book.title, "author": book.author, "available": book.available}})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route for deleting a book
@app.route('/library/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"success": True, "message": "Book deleted"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# For Bonus
# Route for searching books by title and/or author
@app.route('/library/books/search', methods=['GET'])
def search_books():
    try:
        title = request.args.get('title')
        author = request.args.get('author')
        query = Book.query

        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
        
        books = query.all()
        return jsonify([{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books])
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
