from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///urls.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def index():
    return "Welcome to the URL shortener!"

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']
    short_url = original_url.split('//')[-1]  # Simplified short URL generation
    new_link = URL(original_url=original_url, short_url=short_url)
    db.session.add(new_link)
    db.session.commit()
    return f'Short URL is: {url_for("redirect_to_url", short_url=short_url, _external=True)}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

