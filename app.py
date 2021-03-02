from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import nba_api_helper
import MySQLdb
import re
import os

app = Flask(__name__)

def dbConnect():
    return MySQLdb.connect(host="private",
                        user="private",
                        password="ptivate",
                        db="private")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in  session:
            return f(*args, **kwargs)
        else:
            flash("Please login to see this page", "danger")
            return redirect(url_for("login"))
    return wrap

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game',methods=['GET','POST'])
@is_logged_in
def about():
    if request.method == 'GET':
        session['correct'] = 0
        session['incorrect'] = 0
        session['streak'] = 0
        data = nba_api_helper.get_random_player_data()
        session['answer'] = data[0]
        session['answer_2'] = data[1]

        return render_template("game.html", data=data)
    else:
        user_guess = re.sub('[^A-Za-z0-9]+', '', request.form['name'])
        correct_answer = re.sub('[^A-Za-z0-9]+', '', session['answer'])
        correct_answer2 = session['answer_2']

        if (user_guess.lower() == correct_answer.lower()) or (user_guess.lower() == correct_answer2.lower()):
            session['correct'] = session['correct']+1
            session['incorrect'] = session['incorrect']+1
            session['streak'] = session['streak']+1
            data = nba_api_helper.get_random_player_data()
            session['answer'] = data[0]
            session['answer_2'] = data[1]

            flash("That is correct!","success")
            return render_template("game.html", data=data)
        else:
            session['last_score'] = session['correct']
            session['correct'] = 0
            session['incorrect'] = 0
            session['streak'] = 0
            data = nba_api_helper.get_random_player_data()
            session['answer'] = data[0]
            session['answer_2'] = data[1]
            flash("That is incorrect! Hit this button to submit your score!", "danger")
            return render_template("game.html", data=data)

@app.route('/high-scores',methods=['GET', 'POST'] )
def scores():
    db = dbConnect()
    if request.method == "GET":
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10;")
        scores = cur.fetchall()

        if result > 0:
            return render_template('scores.html', scores=scores)
        else:
            msg = 'No scores found'
            return render_template('scores.html', msg=msg)
        cur.close
    else:
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        username = session["username"]
        score = str(session["last_score"])
        result = cur.execute("INSERT INTO `scores` (`id`, `username`, `score`, `create_date`) VALUES (NULL, %s, %s, CURRENT_TIMESTAMP);", (username, score))
        cur.close
        db.commit()
        flash("Your score has been subitted", "success")
        return redirect(url_for('scores'))
    db.close()

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=7, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    db = dbConnect()
    cur = db.cursor()

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",(name,email,username,password))

        db.commit()
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    cur.close()
    db.close()
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    db = dbConnect()
    cur = db.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        username = request.form["username"]
        password_candidate = request.form["password"]

        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash("You are now logged in", "success")

                return redirect(url_for('dashboard'))

            else:
                error = "Invalid password."
                return render_template("login.html",error=error)
        else:
            error = "Username not found."
            return render_template("login.html",error=error)


    cur.close()
    db.close()
    return render_template('login.html' )

@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", 'success')

    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
        db = dbConnect()
        if request.method == "GET":
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            result = cur.execute("SELECT * FROM scores WHERE username = %s ORDER BY score DESC LIMIT 10", [session["username"]])
            scores = cur.fetchall()

            if result > 0:
                return render_template('dashboard.html', scores=scores)
            else:
                msg = 'No scores found'
                return render_template('dashboard.html', msg=msg)
        cur.close()
        db.close()


if __name__ == '__main__':
    app.secret_key = 'super secret key'

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
