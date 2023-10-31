from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a cafe location
class CreateCafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    has_sockets = BooleanField("Electrical Sockets")
    has_toilet = BooleanField("WC")
    has_wifi = BooleanField("WiFi")
    can_take_calls = BooleanField("Meetings Allowed")
    map_url = StringField("Map URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    lat = FloatField("Latitude", validators=[DataRequired()])
    lon = FloatField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Submit")
