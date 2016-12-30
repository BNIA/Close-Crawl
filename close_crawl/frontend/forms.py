from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, RadioField, SelectField, StringField
from wtforms.fields.html5 import DecimalRangeField

from .config import CASE_TYPE, CASE_YEAR


class ScrapeForm(Form):

    case_type = RadioField(
        'Type of case',
        default=CASE_TYPE[0][0],
        choices=CASE_TYPE
    )
    case_year = SelectField('Case Year', choices=CASE_YEAR)
    lower_bound = DecimalRangeField('Lower bound', default=1)
    upper_bound = DecimalRangeField('Upper bound', default=1)
    output = StringField('Output', default="output.csv")
    debug = BooleanField('Debug', default=False)
    anon = BooleanField('Anonymize', default=False)
