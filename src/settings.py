"""settings.py

Configuration settings and variables for the project"""

HEADER = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
URL = 'http://casesearch.courts.state.md.us/casesearch//inquiry-index.jsp'

HTML_DIR = 'responses'
HTML_FILE = HTML_DIR + '/{case}'

# hardcoded cases
CASES = ['24O14000003', '24O14000013',
         '24O14000017', '24O14000041', '24C14000041']


FEATURES = [
    'Filing Date',
    'Case Number',
    'Case Type',
    'Title',
    'Plaintiff',
    'Defendant',
    'Address',
    'Zip Code',
    # 'Business or Organization Name:'  # for partial cost...?
]
