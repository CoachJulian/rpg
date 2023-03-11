from flask import Flask, request,render_template, redirect, url_for
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

    
    
def verify_user(email,password):
    user = {}

    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    
    result = curs.execute(" SELECT name, email FROM users WHERE email=(?) AND password= (?)", [email,password])
    
    for row in result:
        user = {
            'name' : row[0],
            'email' : row[1],
            
            
        }
    conn.close()
    return user

@app.route('/delete_user' , methods=['POST'])

def delete_user():
    email = request.form['email']
    password = request.form['password']


    conn =sqlite3.connect('./static/data/example_database.db')

    #cursor object which commands are executed by?
    curs = conn.cursor()
    curs.execute("DELETE FROM users WHERE email=(?) and password=(?)",[email,password])
    print("deleted user")


    conn.commit()
    conn.close()
    return render_template('index.html')

    





@app.route('/login_user' , methods=['POST'])

def login_user():

    email = request.form['email']
    password = request.form['password']
    
    data = {}
    user = verify_user(email, password)
    
    
    #print(user)
    
    if user:
        bucket= user['name']
        char_class= grab_stats(bucket)
        print(char_class)
        data = {
            "name": user["name"],
            "class": char_class['char_class']
        }
        print(data)

        #Load home if user exists
        return render_template('homepage.html', data=data)
         

    else: 
        error_msg = "Login failed"

        data = {
            "error_msg": error_msg
        }
        #no user redirects back to login
        #print(data)
        return render_template('index.html', data=data)
def grab_stats(user_stats):
    conn=sqlite3.connect('./static/data/example_database.db')

    email = request.form['email']

    curs = conn.cursor()
    info = curs.execute("SELECT char_class FROM users WHERE email=(?)",[email])
    info = curs.fetchone()

    info={
        'char_class': info[0]
    }


    #try passing in name and email to pull out char_class
    
    
    conn.close()
    print(info)
    return info
@app.route('/post_user', methods =['POST'])
def post_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    pw = request.form['password']
    char_class= request.form['character_class']

    store_user(name, email, phone, pw, char_class)

    users = get_all_users()

    new_user = users.pop()



    return render_template('login.html', user=new_user)

def store_user(name, email, phone, pw, char_class):
    # linking to the databas that was created
    conn =sqlite3.connect('./static/data/example_database.db')

    #cursor object which commands are executed by?
    curs = conn.cursor()
    curs.execute("INSERT INTO users (name, email, phone, password, char_class) VALUES( (?),(?),(?),(?),(?) )", (name, email, phone, pw,char_class))
    
    conn.commit()
    conn.close()




def get_all_users():
    conn = sqlite3.connect('./static/data/example_database.db')
    curs = conn.cursor()
    all_users = [] #empty list to populate
    rows = curs.execute("SELECT * from users") #returns as list "*" is a wildcard decorator for "all"

    for row in rows:
        user = { 
                  'name':  row[0],
                  'email': row[1],
                  'phone': row[2],
                  'char_class': row [3],
                }  
        all_users.append(user) #sauce that adds the user as a dict
    conn.close() #since we are just reading data
    return all_users 



#----------------------add routes--------------------------------------





if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
