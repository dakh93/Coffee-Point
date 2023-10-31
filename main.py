from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import pandas as pd
import folium
from folium.plugins import MarkerCluster

from forms import CreateCafeForm

DATABASE_URI = 'sqlite:///cafes.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    query: db.Query = db.session.query_property()  # this is if we want to have auto-complete
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.Integer)
    coffee_price = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, unique=False, default=True)
    has_toilet = db.Column(db.Boolean, unique=False, default=True)
    has_wifi = db.Column(db.Boolean, unique=False, default=True)
    can_take_calls = db.Column(db.Boolean, unique=False, default=True)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    lat = db.Column(db.Double)
    lon = db.Column(db.Double)

    def __repr__(self):
        return f'<Cafe id: {self.id} name: {self.name} location: {self.location} coffee price: {self.coffee_price}>'


def create_map_with_all_cafes(cafes):
    m = folium.Map(width=600, height=600, location=[51.5161239, -0.0851626], tiles='OpenStreetMap', zoom_start=8)
    marker_cluster = MarkerCluster().add_to(m)
    for cafe in cafes:
        cafe_info = f"{cafe.name}, {cafe.location} \n LAT: {cafe.lat} \n LON: {cafe.lon}"
        folium.Marker(location=[cafe.lat, cafe.lon], popup=cafe_info, icon=folium.Icon(color='red')).add_to(marker_cluster)
    return m


@app.route('/')
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    print(cafes[0])
    cafes_map = create_map_with_all_cafes(cafes)

    return render_template("index.html", all_cafes=cafes, map=cafes_map._repr_html_())
@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_cafes'))


@app.route("/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    edit_form = CreateCafeForm(
        name=cafe.name,
        location=cafe.location,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        lat=cafe.lat,
        lon=cafe.lon
    )
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.location = edit_form.location.data
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data
        cafe.has_sockets = edit_form.has_sockets.data
        cafe.has_toilet = edit_form.has_toilet.data
        cafe.has_wifi = edit_form.has_wifi.data
        cafe.can_take_calls = edit_form.can_take_calls.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.lat = edit_form.lat.data
        cafe.lon = edit_form.lon.data

        db.session.commit()
        return redirect(url_for("get_all_cafes"))
    return render_template("create-cafe.html", cafe=cafe, form=edit_form, is_edit=True)


if __name__ == "__main__":
    app.run(debug=True, port=5001)


# # READ ALL RECORDS
# with app.app_context():
#     result = db.session.execute(db.select(Cafe).order_by(Cafe.id))
#     all_cafes = result.scalars()
#     for cafe in all_cafes:
#         print(cafe)

#
# # Create table schema in the database. Requires application context.
# with app.app_context():
#     db.create_all()


# #CREATE RECORD
# with app.app_context():
#     new_book = Book(title="Red Hat", author="Unknown", rating=8.7)
#     db.session.add(new_book)
#     db.session.commit()

# ----------------------------------------------------------------------------

# # READ PARTICULAR RECORD
# with app.app_context():
#     book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
#     print(book.title)

# ----------------------------------------------------------------------------

# UPDATE PARTICULAR RECORD
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.title == "Rich Poor Dad")).scalar()
#     book_to_update.title = "Rich Poor Dad(2018)"
#     db.session.commit()
#     print(book_to_update)

# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.id == 3)).scalar()
#     book_to_update.rating = 5.7
#     db.session.commit()

# ----------------------------------------------------------------------------

# DELETE RECORD
# with app.app_context():
#     book_id = 2
#     # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     book_to_delete = db.get_or_404(Book, book_id)
#     db.session.delete(book_to_delete)
#     db.session.commit()