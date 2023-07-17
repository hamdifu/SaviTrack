from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import RegisterForm,LoginForm,TrackForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from trackprice import ScrapeData
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SaviTrack'
Bootstrap(app)
##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///trackit1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable= False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100),nullable=False,unique=True)
    links = relationship("Links",back_populates="author")
#
class Links(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    product_url = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Integer,nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", back_populates="links")

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already exists! Try logging in instead.")
            return redirect(url_for('login'))
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256',salt_length=8),
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email does not exist, try again!!")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, form.password.data):
            flash("Incorrect password! Try again!!")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template("login.html", form=form,logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/tracklist')
def tracklist():
    links = Links.query.filter_by(author=current_user)
    return render_template("item.html", links=links, logged_in=current_user.is_authenticated)

@app.route('/',methods=['GET', 'POST'])
def home():
    form = TrackForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login!")
            return redirect(url_for('register'))
        sc = ScrapeData()
        data = sc.start(form.url.data)
        new_link = Links(
            product_url=form.url.data,
            budget=form.budget.data,
            price=data[0],
            title=data[1],
            author=current_user
        )
        db.session.add(new_link)
        db.session.commit()
        return redirect(url_for("tracklist"))
    return render_template("index.html", form=form, is_edit=False, logged_in=current_user.is_authenticated)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



