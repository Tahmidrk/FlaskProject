from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
import os

app = Flask(__name__)
# Use environment variable for database URL in production, fallback to local MySQL for development
database_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:@localhost/flaskproject')
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    msg = db.Column(db.String(120), nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        date = request.form.get('date')
        message = request.form.get('message')

        entry = Contacts(name=name, email=email, phone_num=phone_num, date=datetime.now(), msg=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route("/post")
def post():
    # Sample post data
    post_data = {
        'title': 'Sample Blog Post',
        'date': 'June 12, 2025',
        'content': '''
        <p>This is a sample blog post content. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        
        <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
        
        <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        '''
    }
    return render_template('post.html', post=post_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the tables
    app.run(host='0.0.0.0', port=5000, debug=False)