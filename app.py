from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Connection Configuration
DB_CONFIG = {
    'host': 'your_mysql_host',  # e.g., 'localhost' or the external provider's IP
    'user': 'your_mysql_user',  # e.g., 'root' or your MySQL username
    'password': 'your_mysql_password',  # your MySQL password
    'database': 'your_database_name',  # the database name you are using
}

# Nuur khudgas: Medeelel gargah
@app.route('/')
def index():
    # Connecting to MySQL Database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # Get books data
    cursor.execute("SELECT * FROM Books")
    books_data = cursor.fetchall()
    
    # Get top-selling books from the view
    cursor.execute("SELECT * FROM Top_Selling_Books")
    top_selling_books = cursor.fetchall()

    conn.close()
    return render_template('index.html', books=books_data, top_selling_books=top_selling_books)

# Add new book
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        genre_id = request.form['genre_id']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']
        publication_year = request.form['publication_year']
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insert book into Books table
        cursor.execute(
            "INSERT INTO Books (title, author_id, genre_id, price, stock_quantity, publication_year) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (title, author_id, genre_id, price, stock_quantity, publication_year)
        )
        
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

# Edit book details
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        genre_id = request.form['genre_id']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']
        publication_year = request.form['publication_year']
        
        # Update book in the Books table
        cursor.execute(
            "UPDATE Books SET title=%s, author_id=%s, genre_id=%s, price=%s, stock_quantity=%s, "
            "publication_year=%s WHERE book_id=%s",
            (title, author_id, genre_id, price, stock_quantity, publication_year, book_id)
        )
        
        conn.commit()
        conn.close()
        return redirect('/')
    
    cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    return render_template('edit.html', book=book)

# Delete book
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete(book_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Delete book from the Books table
    cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))
    
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
