from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from supabase import create_client, Client

MOVIE_DB_API_KEY = os.environ.get('MOVIE_DB_API_KEY')
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

# define supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    result = supabase.table("movie").select("*").order("rating", desc=False).limit(10).execute()

    all_movies = result.data  # convert ScalarResult to Python List
    print(all_movies)

    for i in range(len(all_movies)):
        all_movies[i]["ranking"] = len(all_movies) - i
    supabase.table("movie").upsert(all_movies).execute()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)

    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = supabase.table("movie").select("*").eq('id', movie_id).execute()
    if form.validate_on_submit():
        supabase.table("movie").update({'rating': float(form.rating.data)}).eq('id', movie_id).execute()
        supabase.table("movie").update({'review': str(form.review.data)}).eq('id', movie_id).execute()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie.data, form=form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    supabase.table("movie").delete().eq('id', movie_id).execute()
    return redirect(url_for("home"))


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        movie_ins = (supabase.table("movie")
                    .insert({"title": data["title"],
                             "year": data["release_date"].split("-")[0],
                             "img_url": f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
                             "description": data["overview"]
                             }
                            )
                    .execute())
        return redirect(url_for("rate_movie", id=int(movie_ins.data[0]["id"])))


if __name__ == '__main__':
    app.run(debug=True)
