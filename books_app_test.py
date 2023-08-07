import sys
import mysql.connector
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

db_host = os.environ["INSTANCE_HOST"]
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_port = os.environ["DB_PORT"]

try:
    db = mysql.connector.connect(host = db_host, user = db_user, password = db_pass, port = db_port, autocommit=True)
except Exception as e:
    print("Error:" + str(e))
    sys.exit(0)

conn = db
cursor = conn.cursor()

cursor.execute('''
    USE books  
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
''')
conn.commit()

def add_book(title, author):
    cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
    conn.commit()

def get_books():
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()

def delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()

def close_connection():
    cursor.close()
    conn.close()

@app.route('/')
def index():
    allBooks = get_books()
    return render_template('index.html', all_books=allBooks)

@app.route("/add_book", methods=["POST", "GET"])
def AddBook():
    if request.method == "POST":
        title_value = request.form["title_input"]
        author_value = request.form["author_input"]
        add_book(title_value, author_value)
        allBooks = get_books()
        return redirect(url_for('index'))
    else:
        return render_template('add_book.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
