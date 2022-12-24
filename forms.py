from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class question(FlaskForm):
    field = StringField("Field", validators = [InputRequired(), Length(max=20)])
    submit = SubmitField('Search by name')