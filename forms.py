from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, Optional

class question(FlaskForm):
    field = StringField("field", validators = [InputRequired(), Length(max=20)])
    year = RadioField("field_year", choices=('FF', 'FR', 'SO', 'JR', 'SR', 'UN', 'GR'), validators=[Optional()])
    submit = SubmitField('Look up')