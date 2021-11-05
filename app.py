from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

ENV = 'dev'
load_dotenv()

root_pass = os.getenv('ROOT_PASSWORD')
dev_database = 'postgresql://postgres:' + root_pass + '@localhost/productfeedback'
production_database = ''

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = dev_database
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = production_database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    manager = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, manager, rating, comments):
        self.customer = customer
        self.manager = manager
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods={'POST'})
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        manager = request.form['manager']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or manager == '':
            return render_template('index.html', message="Please enter required fields")
        if db.session.query(Feedback).filter(Feedback.customer==customer).count() == 0:
            data = Feedback(customer, manager, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message="Review already submitted for this user")


if __name__ == '__main__':
    app.debug = True
    app.run()