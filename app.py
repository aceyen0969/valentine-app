from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# ----- FLASK APP SETUP -----
app = Flask(__name__)
app.config['SECRET_KEY'] = 'valentine_secret'

# Use absolute path for SQLite for Render
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
db = SQLAlchemy(app)

# ----- DATABASE MODEL -----
class Confession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# ----- ROUTES -----
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/confessions', methods=['GET', 'POST'])
def confessions():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            new_confession = Confession(message=message)
            db.session.add(new_confession)
            db.session.commit()
        return redirect('/confessions')

    all_confessions = Confession.query.order_by(Confession.date_posted.desc()).all()
    return render_template("confessions.html", confessions=all_confessions)

# ----- ENSURE DATABASE EXISTS -----
with app.app_context():
    db.create_all()

# ----- LOCAL DEVELOPMENT -----
if __name__ == '__main__':
    app.run()
