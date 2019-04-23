# Script sends an email with different photo to people from the mailing list everyday.

import smtplib
import ssl
import time
import traceback
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# allows to update mailing list without stopping program
def mailing_list():
    with open('email_list.txt', 'r+') as emails:
        email_list = emails.read()
    return email_list.split()


# main function which sends email everyday (every 86400 seconds)
def send_mail(delay):
    # SMTP - static connection details
    port = 000  # port
    smtp_server = ""  # server
    sender = ""  # sender email
    password = ""  # password
    context = ssl.create_default_context()

    i = 1  # days
    while i < 366:
        time.sleep(delay)  # main loop

        # Picks every address from file and sends message to each person from list.
        # None of the person knows who else received an email.
        for email in mailing_list():
            # MIME - dynamic details
            msg = MIMEMultipart()
            msg['From'] = f'{sender}'
            msg['To'] = f'{email}'
            msg['Subject'] = f'Day {i}'
            msg.preamble = f'Day {i}'

            # SMTP - receiver
            receiver = f'{email}'

            # Attaching photo from pics folder
            with open(f'pics/pic{i}.jpg', 'br') as f:
                img = MIMEImage(f.read(), _subtype='jpg')
            msg.attach(img)

            smtp_obj = smtplib.SMTP_SSL(host=smtp_server, port=port,
                                        context=context)
            smtp_obj.login(sender, password)  # establishing connection with server
            try:
                smtp_obj.sendmail(sender, receiver, msg.as_string())  # trying to send an email
                print("---------sended!---------")
            except:
                traceback.print_exc()
            finally:
                smtp_obj.close()
        i += 1  # days incrementation
