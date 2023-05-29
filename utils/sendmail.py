import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formataddr
import os

class Sendmail():
    def send_email(recipient_email, subject, message):

        sender_email = "smbank23@gmail.com"
        sender_id = 'SM Bank'
        password = "fikezdlfxuvqacrc"
        recipient_email = recipient_email
        subject = subject
        message = message

        # Set up the message content
        #msg = MIMEText(message)
        msg = MIMEMultipart('related')
        #msg = MIMEText("Welcome to SMbank")
        msg['Subject'] = subject
        msg['From'] = formataddr((sender_id, sender_email))
        msg['To'] = recipient_email

        msg.attach(MIMEText(message, 'html'))

        # Attach the image file
        current_directory = os.getcwd()
        current_dir = current_directory + '/utils/'
        file_name = 'signature-logo.jpg'
        with open(os.path.join(current_dir, file_name), 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<image1>')
            msg.attach(img)


        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        #mail_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return 'Email sent successfully!'
