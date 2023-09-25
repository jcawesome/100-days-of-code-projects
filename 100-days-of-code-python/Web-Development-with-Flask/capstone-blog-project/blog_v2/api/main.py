from flask import Flask, render_template
import requests

blog_url = 'https://api.npoint.io/eb6cd8a5d783f501ee7d'
blog_resp = requests.get(blog_url)
posts = blog_resp.json()


app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<int:p_id>')
def get_post(p_id):
    post = posts[p_id - 1]
    return render_template('post.html', post=post, image=post['image_url'])


if __name__ == "__main__":
    app.run(debug=True)