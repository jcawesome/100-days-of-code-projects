from flask import Flask, render_template
import random
from datetime import datetime, date
import requests

app = Flask(__name__)


@app.route('/')
def home():
    random_number = random.randint(1, 10)
    today = date.today()
    current_year = today.year
    return render_template("index_basic.html", num=random_number, copyright_year=current_year)


@app.route('/guess/<name>')
def guess(name=None):
    genderize = requests.get('https://api.genderize.io?name=peter').json()
    gender_guess = genderize["gender"]

    agify = requests.get('https://api.agify.io?name=michael').json()
    age_guess = agify["age"]
    return render_template("guess.html", name=name, gender=gender_guess, age=age_guess)


@app.route('/blog/<num>')
def get_blog(num):
    blog_url = 'https://api.npoint.io/5f7219cdcf435c25e5b4'
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)
