from flask import Flask, render_template, redirect,request,url_for
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user='root',
    password='root',
    database='crud_db')
cursor = conn.cursor()


# Check if the connection is successful
if conn.is_connected():
    cursor.execute("SELECT * FROM users")
    users=cursor.fetchall()
    print("Connected to MySQL database")
    print(users)

@app.route('/',methods=['GET', 'POST'])
def index():
    # CREATE
    if request.method == 'POST':
        if request.form['action'] == 'add':
            name = request.form['name']
            gender = request.form['gender']
            mobile_number = request.form['mobile_number']
            if conn :
                cursor.execute("INSERT INTO users (name,gender,mobile_number) VALUES (%s,%s,%s)", (name, gender, mobile_number))
                conn.commit()
                cursor.execute("SELECT * FROM users")
                users=cursor.fetchall()
                print("User added successfully",users,flush=True)

        # UPDATE
        elif request.form['action'] == 'update':
            print("Updating user")
            user_id = request.form['user_id']
            name = request.form['name']
            gender = request.form['gender']
            mobile_number = request.form['mobile_number']
            if conn :
                cursor.execute("UPDATE users SET name=%s, gender=%s, mobile_number=%s WHERE user_id=%s", (name, gender,mobile_number, user_id))
                conn.commit()
                print("User updated successfully")
    
    # READ
    if conn:
        cursor.execute("SELECT * FROM users")
        users=cursor.fetchall()
        return render_template('index.html', users=users)

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM users WHERE user_id = %s", (id,))
    conn.commit()
    print("User deleted successfully")
    return redirect('/')

# PREFILL UPDATE FORM
@app.route('/edit/<int:id>')
def edit(id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (id,))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users, edit_user=user)

if __name__=='__main__':
    app.run(debug=True)
