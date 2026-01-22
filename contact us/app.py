from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__  )
app.secret_key = "mysecretkey"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@#$admin1234",
        database="contact"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # insert data
    if request.method == "POST":
        name = request.form ['name']
        email = request.form ['email']
        phone = request.form ['phone']
        course = request.form ['course']
        address = request.form ['address']
        message = request.form ['message']
        cursor.execute("INSERT INTO student (name,email,phone,course,address,message) VALUES (%s,%s,%s,%s,%s,%s)", (name,email,phone,course,address,message))
        conn.commit()
        flash('Data inserted successfully')
        return redirect('/')
    
    # display data
    cursor.execute("SELECT * FROM student")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html" , data=data)
   
   # delete record
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student where id=%s", (id,))
    conn.commit()
    cursor.close()
    flash('record delete successfully')
    return redirect ('/')

# edit
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student where id=%s", (id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    flash('edit record successfully')
    return render_template('edit.html', record=record)

# update
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form ['name']
    email = request.form ['email']
    phone = request.form ['phone']
    course = request.form ['course']
    address = request.form ['address']
    message = request.form ['message']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE  student set name=%s, email=%s, phone=%s, course=%s, address=%s, message=%s where=id%s", (name,email,phone,course,address,message,id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Record update successfully')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)