import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration

class Cafe(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(250), unique=True, nullable=False)
    map_url: str = db.Column(db.String(500), nullable=False)
    img_url: str = db.Column(db.String(500), nullable=False)
    location: str = db.Column(db.String(250), nullable=False)
    seats: str = db.Column(db.String(250), nullable=False)
    has_toilet: bool = db.Column(db.Boolean, nullable=False)
    has_wifi: bool = db.Column(db.Boolean, nullable=False)
    has_sockets: bool = db.Column(db.Boolean, nullable=False)
    can_take_calls: bool = db.Column(db.Boolean, nullable=False)
    coffee_price: str = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def random_cafe():
    cafe = random.choice(Cafe.query.all())
    return jsonify(cafe.to_dict())


@app.route("/all", methods=["GET"])
def all_cafes():
    cafes_list = Cafe.query.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes_list])


@app.route("/search", methods=["GET"])
def search_cafe():
    location = request.args.get("loc")
    cafes_list = Cafe.query.where(Cafe.location == location).all()
    if cafes_list:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes_list])
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a cafe at that location"}), 404
    return jsonify()


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("has_sockets")),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        print(new_price)
        cafe.coffee_price = new_price
        print(cafe.can_take_calls)
        print(cafe.coffee_price)
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price"}), 200
    else:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database"}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
