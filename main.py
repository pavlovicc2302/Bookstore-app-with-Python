from flask import Flask, render_template, request
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
                   image TEXT)
                   """)
    mysql.connection.commit()
    cursor.close()

# GET metoda - vraca sve knjige koje postoje u biblioteci
@app.route("/")
def books():
    create_table_books()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    cursor.close()
    return render_template("books.html", books = books)

if __name__ == "__main__":
    app.run(debug=True)