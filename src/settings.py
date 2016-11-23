"""settings.py

Configuration settings and variables for the project"""

HEADER = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
URL = 'http://casesearch.courts.state.md.us/casesearch//inquiry-index.jsp'
CASE_PAT = '24{type}{year}00{num}'

# TODO: change dir after debug
# HTML_DIR = 'debug/responses_debug/'
HTML_DIR = 'responses/'
HTML_FILE = HTML_DIR + '/{case}'

FINAL_DATASET = "../datasets/{dir}/{year}.csv"

CASE_ERR = 'logs/case_error.txt'
SAVE_PROG = 'logs/save_progess.txt'

FEATURES = [
    'Filing Date',
    'Case Number',
    'Case Type',
    'Title',
    'Plaintiff',
    'Defendant',
    'Address',
    'Business or Organization Name',
    'Party Type',
]

FIELDS = FEATURES + [
    'Zip Code',
    'Partial Cost',
]

INTERNAL_FIELDS = [
    'Business or Organization Name',
    'Party Type',
]
