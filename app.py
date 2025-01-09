from flask import Flask, render_template, request ,redirect ,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager , login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'MITS@123'


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


app.app_context().push()
db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user:
            flash ("User already exists")
            return redirect(url_for('signup'))
        hashed_password=generate_password_hash(password,method='pbkdf2:sha256')
        user=User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('viewplayer'))
        flash("Invalid username or password")
        return redirect(url_for('login'))
    return render_template("login.html")



@app.route('/')
def hello():
    return render_template("home.html")



@app.route('/about')
def about():
    name="Bhavya"
    age= 20
    runs=[12,34,45,56,87,67]
    return render_template("index.html",name=name,age=age,runs=runs)


@app.route('/about/contact')
def contact():
    return render_template("contact.html")

@app.route('/userdetails/<int:id>')
def userdetails(id):
    return f"User id is : {id}"



@app.route('/addplayer',methods=['GET','POST'])
def addplayer():
    if request.method== 'POST':
        name=request.form['name']
        age=request.form['age']
        p1=Player(name=name,age=age)
        db.session.add(p1)
        db.session.commit()
        return redirect(url_for('viewplayer'))
    return render_template("addplayer.html")



@app.route('/viewplayer')
def viewplayer():
    players=Player.query.all()
    return render_template("viewplayer.html",players=players)

@app.route('/editplayer/<int:id>',methods=['GET','POST'])
def editplayer(id):
    if request.method=='POST':
        player=db.session.get(Player,id)
        player.name=request.form['name']
        player.age=request.form['age']
        db.session.commit()
        return redirect(url_for('viewplayer'))
    player=Player.query.get(id)
    return render_template("editplayer.html",id=id,player=player)


@app.route('/deleteplayer/<int:id>')
def deleteplayer(id):
    player=Player.query.get(id)
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('viewplayer'))



@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


app.run(debug=True)
