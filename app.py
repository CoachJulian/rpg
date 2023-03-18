from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/delete_user', methods=['POST'])
def delete_user():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    curs.execute("DELETE FROM users WHERE email = ? AND password = ?", (email, password))
    print("deleted user")

    conn.commit()
    conn.close()

    return render_template('index.html')




@app.route('/edit_user', methods=['POST'])
def edit_user():
    new_class = request.form['character_class']
    rowid = request.form['rowid']

    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    
    curs.execute("UPDATE users SET char_class = (?) WHERE rowid =?",(new_class,rowid))
    print("edited user")

    conn.commit()
    conn.close()

    return render_template('index.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    curs.execute("SELECT rowid, name, email FROM users WHERE email = ? AND password = ?", (email, password))
    row = curs.fetchone()
    conn.close()

    if row:
        rowid, name, email = row
        char_class = grab_stats(rowid)
        print(char_class)
        data = {
            "rowid": rowid,
            "name": name,
            "class": char_class['char_class']
            }
        print(data)

# Load home if user exists
        return render_template('homepage.html', data=data)

    else:
        error_msg = "Login failed"
        data = {"error_msg": error_msg}

# No user redirects back to login
# print(data)
        return render_template('index.html', data=data)



@app.route('/post_user', methods=['POST'])
def post_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    pw = request.form['password']
    char_class = request.form['character_class']

    store_user(name, email, phone, pw, char_class)

    users = get_all_users()
    new_user = users.pop()

    return render_template('login.html', user=new_user)

def store_user(name, email, phone, pw, char_class):
    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO users (name, email, phone, password, char_class) VALUES (?, ?, ?, ?, ?)", (name, email, phone, pw, char_class))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    all_users = []
    rows = curs.execute("SELECT rowid, name, email, phone, char_class FROM users")

    for row in rows:
        user = {
            'rowid': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'char_class': row[4],
        }
        all_users.append(user)

    conn.close()

    return all_users


def grab_stats(rowid):
    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    info = curs.execute("SELECT char_class FROM users WHERE rowid = ?", (rowid,))
    info = curs.fetchone()
    info = {'char_class': info[0]}

    conn.close()
    print(info)

    return info

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
