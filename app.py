import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'valentine_secret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "site.db")}'
db = SQLAlchemy(app)

class Confession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/confessions', methods=['GET', 'POST'])
def confessions():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            new_confession = Confession(message=message)
            db.session.add(new_confession)
            db.session.commit()
        return redirect('/confessions')

    all_confessions = Confession.query.order_by(Confession.date_posted.desc()).all()
    return render_template("confessions.html", confessions=all_confessions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
