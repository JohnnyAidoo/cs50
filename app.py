from flask import Flask , render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# bcrpyt
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))


class Note(db.Model):
    id = db.Column(db.Integer,  primary_key = True)
    authur = db.Column(db.String(300))
    


@app.route('/')
def home():
    user = User.query.filter_by(id = 1).first()
    if user:
        user_name = user.name

    return(render_template('index.html', name = user_name))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # get user inputs
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password)

        # create a new usera
        new_user = User(name=name, email=email , password=hashed_password)

        # add new user to database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))
    return(render_template('signup.html'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        #get user input
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email = email).first()
        if user and bcrypt.check_password_hash(user.password , password):
            return redirect(url_for('home'))
        else:
            return
    return(render_template('login.html'))

# 



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)