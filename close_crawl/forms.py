from flask_wtf import Form
from wtforms import BooleanField, RadioField, StringField, SelectField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields.html5 import DecimalRangeField
from modules import settings


class ScrapeForm(Form):

    case_type = RadioField(
        'Type of case',
        default=settings.CASE_TYPE[0][0],
        choices=settings.CASE_TYPE
    )
    case_year = SelectField('Case Year', choices=settings.CASE_YEAR)
    lower_bound = DecimalRangeField('Lower bound', default=1)
    upper_bound = DecimalRangeField('Upper bound', default=1)
    output = StringField('Output', default="output.csv")
    debug = BooleanField('Debug', default=False)
    anon = BooleanField('Anonymize', default=False)
