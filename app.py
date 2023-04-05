from flask import Flask, render_template, request, redirect, session, url_for
from firebase import auth, db
import secrets, random, string
from datetime import datetime
from collections import OrderedDict

def generate_random_string(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def sort_dict_by_date_created(dictionary):
    sorted_items = sorted(dictionary.items(), key=lambda x: datetime.fromisoformat(x[1]['date_created']))
    sorted_dict = OrderedDict(sorted_items)
    return sorted_dict

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

@app.route('/')
def index():
    if 'username' in session:
        posts = db.child('posts').get().val()
        id = list(sort_dict_by_date_created(posts))[-1]
        return redirect('/' + id)
    else:
        return redirect('/login')
    
@app.route('/<id>')
def index_id(id):
    post = dict(db.child('posts').order_by_child('id').equal_to(id).get().val())
    username = session['username']
    posts = db.child('posts').get()
    return render_template(
        "index.html",
        post = post,
        username = username,
        posts = dict(posts.val()),
        id = id
    )

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email = username + '@gmail.com', password = password)
            session['username'] = username
            return redirect('/')
        except:
            return render_template(
                    'login.html',
                    message = "Something went wrong."
            )
    else:
        return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirm-password']
        if password == confirmPassword:
            try:
                auth.create_user_with_email_and_password(email = username + '@gmail.com', password = password)
                session['username'] = username
                return redirect('/')
            except:
                return render_template(
                    'signup.html',
                    message = "Something went wrong."
                )
        else:
            return render_template(
                    'signup.html',
                    message = "Password doesn't matches"
            )
    else:
        return render_template('signup.html')

@app.route("/writePost")
def writePost():
    return redirect(url_for("write"))

@app.route("/post", methods = ['POST', 'GET'])
def post():
    heading = request.form.get('heading')
    content = request.form['content']
    id = generate_random_string()
    author = session['username']
    date_created = str(datetime.now())
    db_update = db.child('posts').child(id).set({
        "id": id,
        "title": heading, 
        "body": content, 
        "author":author, 
        "date_created" : date_created
    })
    if db_update:
        return redirect('/' + id)
    else:
        return redirect('/write.html')

@app.route('/write', methods = ['GET', 'POST'])
def write():
    return render_template('write.html')

if __name__ == '__main__':
    app.run(debug = True)