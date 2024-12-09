
# Library Management API

This is a Flask-based REST API for managing a library system. It allows you to add, update, retrieve, and delete members and books in the library. The app is connected to a MySQL database, where member and book information is stored.

## Features

- Add new members and books
- Retrieve all members and books
- Retrieve, update, and delete specific members and books by ID
- Search for books by title and/or author
- Error handling for 404 (Not Found) and 500 (Internal Server Error)

## Prerequisites

- Python 3.8 or higher
- MySQL or MariaDB server
- `pip` (Python package installer)

## Setup Instructions

Follow these steps to set up the application on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/library-management-api.git
cd library-management-api
```

### 2. Create a virtual environment

It’s a good practice to use a virtual environment to isolate the project dependencies:

```bash
python -m venv venv
```

### 3. Activate the virtual environment

- **Windows:**

```bash
venv\Scripts\activate
```

- **Mac/Linux:**

```bash
source venv/bin/activate
```

### 4. Install required dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the database

Ensure you have MySQL or MariaDB installed on your system. Create a database for the library system and configure the database URI in the `app.py` file:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://username:password@localhost/library"
```

Replace `username`, `password`, and `localhost` with your MySQL credentials and host information.

### 6. Run the Flask application

To start the Flask application, use the following command:

```bash
flask run
```

The application will run by default at `http://127.0.0.1:5000/`.

### 7. Test the API

You can test the API endpoints using tools like **Postman** or **cURL**. The following routes are available:

- **POST /library/members** - Add a new member
- **GET /library/members** - Get all members
- **GET /library/members/<id>** - Get a specific member by ID
- **PUT /library/members/<id>** - Update a member by ID
- **DELETE /library/members/<id>** - Delete a member by ID

- **POST /library/books** - Add a new book
- **GET /library/books** - Get all books
- **GET /library/books/<id>** - Get a specific book by ID
- **PUT /library/books/<id>** - Update a book by ID
- **DELETE /library/books/<id>** - Delete a book by ID

- **GET /library/books/search** - Search books by title and/or author

### 8. Database Initialization

To initialize the database and create the necessary tables, run the following:

```python
from app import db
with app.app_context():
    db.create_all()
```

This will create the `members` and `books` tables in your MySQL database.

## Troubleshooting

- **Error: MySQL Database not found**:
  Make sure that your MySQL server is running and that the `library` database exists. You can create it manually with the following SQL command:

  ```sql
  CREATE DATABASE library;
  ```

- **Error: Missing dependencies**:
  Ensure all dependencies are installed with `pip install -r requirements.txt`.


