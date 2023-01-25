import smtplib
from email.message import EmailMessage
from Credentials import MAIL, PASSWORD


def mail(email:str,filename=''):
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(MAIL, PASSWORD)
    msg = EmailMessage()
    msg["Subject"] = "Good Evening"
    msg["From"] = "Biocluster Archont <archont.biocluster@gmail.com>"
    msg["To"] = email
    # definitely don't mess with the .preamble

    msg.set_content("Wanna some calculations?")

    '''Недописано'''
    if filename != '':
        with open("path/to/attachment.png", "rb") as fp:
            msg.add_attachment(
                fp.read(), maintype="image", subtype="png")

    # Notice how smtplib now includes a send_message() method
    with smtp_server as s:
        s.send_message(msg)
        s.quit()

