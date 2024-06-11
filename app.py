from flask import Flask, request, redirect, render_template
from models import db, Link
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def generate_short_link(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_link = generate_short_link()
        new_link = Link(original_url=original_url, short_link=short_link)
        db.session.add(new_link)
        db.session.commit()
        return render_template('index.html', short_link=short_link)
    return render_template('index.html')

@app.route('/<short_link>')
def redirect_to_url(short_link):
    link = Link.query.filter_by(short_link=short_link).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
