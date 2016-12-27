from flask_wtf import Form
from wtforms import BooleanField, DecimalField, RadioField, SelectField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields.html5 import DecimalRangeField
from modules import settings


class ScrapeForm(Form):

    case_type = RadioField('Type of case',
                           default=settings.CASE_TYPE[0][0],
                           choices=settings.CASE_TYPE)
    case_year = SelectField('case_year', choices=settings.CASE_YEAR)
    lower_bound = DecimalRangeField('Range of cases', default=1)
    upper_bound = DecimalRangeField('Range of cases', default=1)
    debug = BooleanField('Debug', default=False)
    anon = BooleanField('Anonymize', default=False)
