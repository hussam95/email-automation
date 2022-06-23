import smtplib
import mimetypes
from io import BytesIO
from email.message import EmailMessage
import streamlit as st

# Create message and set text content
msg = EmailMessage()
msg['Subject'] = 'This email contains an attachment'
msg['From'] = 'hussam.haq@zembuilders.com'
msg['To'] = 'hussam.haq@zembuilders.com'
# Set text content
msg.set_content('Please see attached file')

def attach_bytesio_to_email(email, buf, filename):
    """Attach a file identified by filename, to an email message"""
    # Reset read position & extract data
    buf.seek(0)
    binary_data = buf.read()
    # Guess MIME type or use 'application/octet-stream'
    maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
    # Add as attachment
    email.add_attachment(binary_data, maintype=maintype, subtype=subtype, filename=filename)

# Attach files
uploaded_files = st.file_uploader(accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    buf = BytesIO()
    buf.write(bytes_data)
    attach_bytesio_to_email(msg, buf, "test.txt")

def send_mail_smtp(mail, host, username, password):
    s = smtplib.SMTP(host)
    s.starttls()
    s.login(username, password)
    s.send_message(msg)
    s.quit()

send_mail_smtp(msg, 'mail.zembuilders.com', 'hussam.haq@zembuilders.com', 'zembuilders@1234')