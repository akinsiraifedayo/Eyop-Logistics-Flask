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
from functions import navigation_items
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os, ssl

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
gravatar=Gravatar(app)

# Configure your email settings
load_dotenv()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your email server
app.config['MAIL_PORT'] = 587  # Replace with the appropriate port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MY_EMAIL') # Replace with your email
app.config['MAIL_PASSWORD'] = os.getenv('MY_PWD')  # Replace with your email password
SUPPORT_MAIL = os.getenv('SUPPORT_MAIL')  # Replace with where all mails should be sent

ssl_context = ssl.create_default_context()
mail = Mail(app)

print(os.getenv('MY_EMAIL'))
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

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    msg_subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

class RequestForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    msg_subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

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

def isValidEmail(email):
    # Basic email validation example (customize as needed)
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)

@app.route('/send-contact-email', methods=["POST"])
def send_contact_email():
    request_form = request.form
    if request.method == "POST":
        try:
            name = request_form['name']
            email = request_form['email']
            phone_number = request_form['phone_number']
            msg_subject = request_form['msg_subject']
            message = request_form['message']

            form_data = ContactForm(name=name, email=email, phone_number=phone_number, msg_subject=msg_subject, message=message)
            db.session.add(form_data)
            db.session.commit()

            msg = Message('New Contact Form Submission', sender=email, recipients=[SUPPORT_MAIL])
            msg.body = f"Name: {name}\nEmail: {email}\nSubject: {msg_subject}\nMessage: {message}"
            msg.reply_to = email
            mail.send(msg)
            flash("Your request has been sent successfully", "success")
        except:
            flash("Please enter valid inputs.", "danger")
            return redirect(request.referrer)
        return redirect(request.referrer)
    else:
        return redirect(url_for('error_404'))

@app.route('/send-quote-email', methods=["POST"])
def send_quote_email():
    request_form = request.form
    if request.method == "POST":
        try:
            transport_type = request_form['transport_type']
            city_of_departure = request_form['city_of_departure']
            city_of_arrival = request_form['city_of_arrival']
            shipment_type = request_form['shipment_type']
            width = request_form['width']
            height = request_form['height']
            weight = request_form['weight']
            length = request_form['width']

            s_name = request_form['s_name']
            s_email = request_form['s_email']
            s_phone_number = request_form['s_phone_number']
            r_name = request_form['r_name']
            r_email = request_form['r_email']
            r_phone_number = request_form['r_phone_number']

            msg = Message('New Quote Request', sender=s_email, recipients=[SUPPORT_MAIL])
            msg.body = (f"Sender Name: {s_name}\nSender Email: {s_email}\nSender Phone: {s_phone_number}\n\n"
                        f"Reciever Name: {r_name}\nReciever Email: {r_email}\nReciever Phone: {r_phone_number}\n\n"
                        f"Transport Type: {transport_type}\nCity of Departure: {city_of_departure}\nCity of Arrival: {city_of_arrival}\n\n"
                        f"Shipment Type: {shipment_type}\nWidth: {width}\nHeight: {height}\nLength: {length}\nWeight: {weight}")
                
            msg.reply_to = s_email
            mail.send(msg)
            sent=True
            flash("Quote Sent Successfully", "success")
            return redirect(f"{request.referrer}?sent=d{sent}")
        except:
            flash("Please enter valid inputs.", "danger")
            return redirect(request.referrer)
    else:
        return redirect(url_for('error_404'))


@app.context_processor
def inject_current_page():
    current_page = request.endpoint
    return dict(current_page=current_page, navigation_items=navigation_items)




@app.route('/coming-soonest', methods=["POST", "GET"])
def coming_soonest():
    subscribed = request.args.get('subscribed', default=False, type=bool)
    if request.method == "POST":
        email = request.form.get("EMAIL")
        if isValidEmail(email):
            # Email is valid
            with open("subscribers.txt", "a") as file:
                file.write(email + "\n")
            return redirect(url_for("coming_soonest", subscribed=True))
        else:
            # Email is not valid
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("coming_soonest"))
            
    return render_template("coming-soon-copy.html", subscribed=subscribed)



@app.route('/', methods=["POST", "GET"])
def home():
    sent = request.args.get("sent")
    return render_template("index.html", sent=sent)

@app.route('/login')
def login():
    return render_template("log-in.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/recover-password')
def recover_password():
    return render_template("recover-password.html")

@app.route('/faq', methods=['POST', 'GET'])
def faq():
    sent = request.args.get("sent")
    # if request.method == 'POST':
    #     send_contact_email(request_form=request.form)

    return render_template("faq.html", sent=sent)

@app.route('/contact', methods=['POST', 'GET'])
def contact_us():
    sent = request.args.get("sent")
    # if request.method == 'POST':
    #     send_contact_email(request_form=request.form)
    
    return render_template("contact-us.html", sent=sent)
    
@app.route('/send-quote')
def send_quote():
    return render_template('expression')


@app.route('/about')
def about():
    sent = request.args.get("sent")
    return render_template("about-us.html", sent=sent)

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





@app.route('/global-location')
def global_location():
    return render_template("global-location.html")



@app.route('/privacy-policy')
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template("terms-conditions.html")

@app.route('/coming-soon')
def coming_soon():
    return render_template("coming-soon.html")


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
    sent = request.args.get("sent")
    return render_template("company.html", sent=sent)


@app.route('/get-quote')
def get_quote():
    return render_template("pricing-style-two.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/404')
def error_404():
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
