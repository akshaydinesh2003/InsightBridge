from flask import Flask, render_template, request ,redirect ,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager , login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'MITS@123'


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='User')  # Default role is 'User'



app.app_context().push()
db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        secret_code = request.form.get('secret_code', None)  # Optional admin code
        
        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists. Please log in.", "error")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Determine role
        role = 'Admin' if secret_code == 'bhavya' else 'User'

        # Create a new user instance
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
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
                return redirect(url_for('dashboard'))
        flash("Invalid username or password")
        return redirect(url_for('login'))
    return render_template("login.html")



@app.route('/')
def hello():
    return render_template("home.html")


#route for dashboard
from flask_login import login_required, current_user

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
        # Fetch admin-specific data
        users = User.query.all()  # Admin can view all users
        return render_template('admin_dashboard.html', users=users)
    else:
        # Fetch user-specific data
        user_data = {
            "username": current_user.username,
            "email": current_user.email,
        }
        return render_template('user_dashboard.html', user_data=user_data)


@app.route('/home')
@login_required
def home():
    return render_template("homnav.html")

@app.route('/tools')
@login_required
def tools():
    return render_template("tools.html")

@app.route('/analytics')
@login_required
def analytics():
    return render_template("analytics.html")


@app.route('/reports')
@login_required
def reports():
    return render_template("reports.html")


@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")



@app.route('/task_manager')
@login_required
def task_manager():
    return render_template('task_manager.html')

@app.route('/invoice_generator')
@login_required
def invoice_generator():
    return render_template('invoice_generator.html')

@app.route('/customer_tracker')
@login_required
def customer_tracker():
    return render_template('customer_tracker.html')

@app.route('/performance_monitor')
@login_required
def performance_monitor():
    return render_template('performance_monitor.html')

@app.route('/team_collaboration')
@login_required
def team_collaboration():
    return render_template('team_collaboration.html')







@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


app.run()
