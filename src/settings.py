"""settings

Configuration settings and variables for the project"""

HEADER = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
URL = 'http://casesearch.courts.state.md.us/casesearch//inquiry-index.jsp'

HTML_DIR = 'responses'
HTML_FILE = HTML_DIR + '/{case}'

# hardcoded cases
CASES = ['24O14000003', '24O14000013', '24O14000017', '24O14000041']


FEATURES = [
    'CASE NUMBER',
    'TITLE',
    'FILING DATE',
    'ADDRESS',
    'ZIP CODE',
    # 'Business or Organization Name:'  # for partial cost...?
]
