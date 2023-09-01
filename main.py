from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever-8BYkEfBA6O6donffddsssszWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
gravatar=Gravatar(app)


##CONFIGURE TABLES

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    posts = db.relationship("BlogPost", back_populates="author")
    comments = db.relationship("Comment", back_populates="author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    
    #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = db.relationship("User", back_populates="posts")
    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", back_populates="blog")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author = db.relationship("User", back_populates="comments")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog = db.relationship("BlogPost", back_populates="comments")
    blog_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    text = db.Column(db.Text, nullable=False)




with app.app_context():
    db.create_all()


# login manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


def admins_only(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if current_user.id == 1:
            return func(*args, **kwargs)
        else:
            return abort(403)
    return decorated_func

@app.route('/coming-soonest')
def coming_soonest():
    #added
    return render_template("coming-soon-copy.html")


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about-us.html")

@app.route('/pricing')
def pricing():
    return render_template("pricing-style-one.html")

@app.route('/testimonials')
def testimonials():
    return render_template("testimonials.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/product-details')
def product_details():
    return render_template("product-details.html")

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/my-account')
def my_account():
    return render_template("my-account.html")



@app.route('/login')
def login():
    return render_template("log-in.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/recover-password')
def recover_password():
    return render_template("recover-password.html")

@app.route('/global-location')
def global_location():
    return render_template("global-location.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/privacy-policy')
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template("terms-conditions.html")

@app.route('/coming-soon')
def coming_soon():
    return render_template("coming-soon.html")

@app.route('/404')
def error_404():
    return render_template("404.html")

@app.route('/services')
def services():
    return render_template("services-style-one.html")

@app.route('/service-details')
def service_details():
    return render_template("services-details.html")

@app.route('/blog')
def blog():
    return render_template("blog-column-one.html")

@app.route('/blog-post')
def blog_post():
    return render_template("blog-details.html")

@app.route('/company')
def company():
    return render_template("company.html")

@app.route('/contact')
def contact_us():
    return render_template("contact-us.html")

@app.route('/get-quote')
def get_quote():
    return render_template("pricing-style-two.html")















@app.route('/register', methods=["POST", "GET"])
def registerz():
    form = RegisterForm()
    if request.method == "POST":
        pwd = form.password.data
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password= generate_password_hash(password=pwd, method="pbkdf2:sha256", salt_length=8)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("Email is registered already, Kindly login instead")
            return redirect(url_for("login"))
        else:
            new_user = db.session.query(User).filter_by(email=form.email.data).first()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
       
    return render_template("register.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def loginz():
    form = LoginForm()
    print("here")
    if request.method == "POST":
        try:
            user=db.session.query(User).filter_by(email=form.email.data).first()
        except:
            flash("This email does not exist")
            return redirect(url_for("login"))
        else:
            is_match = check_password_hash(user.password, form.password.data)
            if is_match:
                login_user(user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Incorrect Password")
                return redirect(url_for("login"))
            
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logoutz():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_postz(post_id):
    requested_post = db.session.query(BlogPost).get(post_id)
    comments =  db.session.query(Comment).filter_by(blog_id=post_id)
    form = CommentForm()
    if request.method == "POST":
        if current_user.is_authenticated:
            comment= Comment(
                author=current_user,
                blog=requested_post,
                text=form.comment.data,
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash("You need to be logged in to post comments")
            return redirect(url_for("login"))
        return redirect(url_for("show_post", post_id=post_id, post=requested_post, form=form, all_comments=comments))
    return render_template("post.html", post=requested_post, form=form, all_comments=comments)


@app.route("/about")
def aboutz():
    return render_template("about.html")


@app.route("/contact")
def contactz():
    return render_template("contact.html")


@app.route("/new-post", methods=["POST", "GET"])
def add_new_postz():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@admins_only
def edit_postz(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        # author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        # post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admins_only
def delete_postz(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
