from __future__ import absolute_import, print_function, unicode_literals

from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.message import MIMEMessage
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText

from frontend import views


if __name__ == '__main__':

    views.app.run(debug=True)
