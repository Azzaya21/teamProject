import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL холболтын тохиргоо
DB_CONFIG = {
    'host': 'sql5.freemysqlhosting.net',
    'user': 'sql5746923',
    'password': 'GNB6i9x4yF',
    'database': '	sql5746923',
}

# Нүүр хуудас: Мэдээллийг харах
@app.route('/')
def index():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")  # Өөрийн хүснэгтийг оруулна
    data = cursor.fetchall()
    conn.close()
    return render_template('./index.html', data=data)

# Мэдээлэл нэмэх
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

# Мэдээлэл засах
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor.execute("UPDATE students SET name = %s, age = %s WHERE id = %s", (name, age, id))
        conn.commit()
        conn.close()
        return redirect('/')
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    record = cursor.fetchone()
    conn.close()
    return render_template('edit.html', record=record)

# Мэдээлэл устгах
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
