from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

# kreiranje flask aplikacije 
app = Flask(__name__)

# povezivanje sa bazom 'biblioteka'
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_DB"] = 'biblioteka'
mysql = MySQL(app)

# kreiranje tabele u bazi
def create_table_books():
    cursor = mysql.connection.cursor()
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS books
                   (id INT AUTO_INCREMENT PRIMARY KEY,
                   title TEXT,
                   author TEXT,
                   publishYear INT,
                   description TEXT,
                   image TEXT)
                   """)
    mysql.connection.commit()
    cursor.close()

# GET metoda - kreira tabelu books i vraca sve knjige koje postoje u bazi
@app.route("/")
def books():
    create_table_books()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    cursor.close()
    return render_template("books.html", books = books)

# POST metoda - dodavanje nove knjige u bazu
@app.route("/add",methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    publishYear = request.form["publishYear"]
    description = request.form["description"]
    image = request.form["image"]
    message = "dodata"

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO books (title, author, publishYear, description, image) VALUES (%s, %s, %s, %s, %s)", (title, author, publishYear, description, image))
    
    mysql.connection.commit()
    cur.close()
    
    return render_template("success.html",message=message)

# Funkcija za dobijanje podataka o knjizi iz baze podataka na osnovu ID-a
def get_book_from_database(book_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cur.fetchone()  
    cur.close()
    
    if book:
        return {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "publishYear": book[3],
            "description":book[4],
            "image": book[5]
        }
    else:
        return None

# Ruta za prikaz forme za azuriranje knjige
@app.route("/update-info/<book_id>", methods=["GET"])
def update_book_form(book_id):

    book = get_book_from_database(book_id)
    if book:
        return render_template("updateBook.html", book=book)
    else:
        return "Knjiga nije pronađena."

# Ruta za brisanje knjige
@app.route("/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    mysql.connection.commit()
    cur.close()
    return render_template("success.html", message="obrisana")

# Ruta za pretragu knjige
@app.route("/search", methods=["GET"])
def search_books():
    query = request.args.get("query")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR publishYear LIKE %s", ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    books = cursor.fetchall()
    cursor.close()
    return render_template("searched.html", books=books, query=query)
    
# Ruta za prikaz detalja knjige
@app.route("/book/<book_id>")
def book_details(book_id):
    book = get_book_from_database(book_id)
    if book:
        return render_template("book.html", book=book)
    else:
        return "Knjiga nije pronađena."


# Ruta za prihvatanje azuriranja podataka o knjizi
@app.route("/update/<book_id>", methods=["post"])
def update_book(book_id):

    title = request.form["title"]
    author = request.form["author"]
    publishYear = request.form["publishYear"]
    description = request.form["description"]
    image = request.form["image"]
    message = "ažurirana"

    cur = mysql.connection.cursor()
    cur.execute("UPDATE books SET title=%s, author=%s, publishYear=%s,description=%s, image=%s WHERE id=%s", (title, author, publishYear,description, image, book_id))
    mysql.connection.commit()
    cur.close()

    return render_template("success.html",message=message)

if __name__ == "__main__":
    app.run(debug=True)