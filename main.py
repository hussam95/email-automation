import smtplib
import mimetypes
from io import BytesIO
from email.message import EmailMessage
import streamlit as st
import os
from PIL import Image
import pandas as pd


pwd = os.getcwd()

# Locating Helper Files Setting Relative Paths to Avoid Hosting Issues
img_path = os.path.join(pwd, "zem.jpg")
csv_path = os.path.join(pwd, "email_record_ZEM.csv")

# Landing Page Image Loading
img = Image.open(img_path)

# Landing Page Col Type Header
col1, col2, col3 = st.columns(3)

with col2:
    st. markdown("<h1 style='text-align: center; color: Green;'>Zem Mail</h1>", unsafe_allow_html=True)
    
with col1:
    st.image(img, width=100)

with col3:
    st.write("")

# Email Groups
email_groups = ["All", "Department Heads", "Admin", "Audit", "Engineering", "Executive", "Finance", "HR", "IT", "Marketing","Operations",
 "Sales -Bahria Enclave", "Sales -GT Road", "Sales -Phase 08"]

# User Selections/Inputs
choice = st.sidebar.selectbox("Select Email Recepient Group", email_groups)
email_sender = st.text_input("Enter Sender's Email")
sender_pass = st.text_input("Enter Sender's password", type="password")
subject = st.text_input("Enter Email's subject")
email_content  = st.text_area("Email Body")


# Email Data Connection
email_data  = pd.read_csv(csv_path)

# Sifitng Email dataframe w.r.t user selection 
if choice == "Finance":
    recipients = email_data[email_data["Deparment"]=="Finance and Accounts"]["Email"].to_list()
elif choice == "Audit":
    recipients = email_data[email_data["Deparment"]=="Audit Compliance"]["Email"].to_list()
elif choice == "Engineering":
    recipients = email_data[email_data["Deparment"]=="Engineering"]["Email"].to_list()    
elif choice == "Operations":
    recipients = email_data[email_data["Deparment"]=="Operations"]["Email"].to_list()
elif choice == "HR":
    recipients = email_data[email_data["Deparment"]=="HR"]["Email"].to_list()
elif choice == "Sales -GT Road":
    recipients = email_data[email_data["Deparment"]=="Sales -GT Road"]["Email"].to_list()
elif choice == "Marketing":
    recipients = email_data[email_data["Deparment"]=="Marketing"]["Email"].to_list()
elif choice == "Quality Assurance":
    recipients = email_data[email_data["Deparment"]=="Quality Assurance"]["Email"].to_list()
elif choice == "IT":
    recipients = email_data[email_data["Deparment"]=="IT"]["Email"].to_list()
elif choice == "Admin":
    recipients = email_data[email_data["Deparment"]=="Admin"]["Email"].to_list()
elif choice == "Procurement and Security":
    recipients = email_data[email_data["Deparment"]=="Procurement and Security"]["Email"].to_list()
elif choice == "Executive Office":
    recipients = email_data[email_data["Deparment"]=="Executive Office"]["Email"].to_list()
elif choice == "All":
    recipients = email_data["Email"].to_list()
elif choice == "Department Heads":
    heads = ["Raja Shiraz Khalid","M. Mohsin Siddiqui", "M. Arslan Asharaf", "Sidra Zaheer",
    "Zeshan Amjad Ali","Arif Nadeem","Amber Nosheen","Sami Ullah Abbasi", "Mazhar Iqbal","M. Rizwan Malik",
    "Akbar Aziz Burqi","Kamil Qamar","Abdul Sattar", "Ismail Haiderr", "Asad Rasheed", "Ahmad Tohaeed Qasmi"]
    recipients = email_data[email_data["Names"].isin(heads)]["Email"].to_list()


# Create message and set text content
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = email_sender
msg['To'] = recipients
# Set text content
msg.set_content(email_content)

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
uploaded_files = st.file_uploader("Choose attachments",accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    buf = BytesIO()
    buf.write(bytes_data)
    attach_bytesio_to_email(msg, buf, uploaded_file.name)

def send_mail_smtp(mail, host, username, password):
    s = smtplib.SMTP(host)
    s.starttls()
    s.login(username, password)
    s.send_message(msg)
    s.quit()


if st.button("Send Mail"):
    try:
        send_mail_smtp(msg, 'mail.zembuilders.com', email_sender, sender_pass)
        st.success(f"{len(recipients)} emails sent successfully to {choice}")
        
    except Exception as e:
        if email_sender == "":
            st.error("Please fill Sender's Email field")
            
        elif sender_pass == "":
            st.error("Please fill Password field")
            
        elif len(recipients) == 0:
            st.error("Please select recipient group from the side bar")
            
        else:
            internet_check = os.system("ping www.google.com")
            if internet_check == 1:
                st.error("Please connect to the internet")
                
            else:
                st.error("Wrong Email or Password")
                

# Copyright 
st.markdown("<i style='text-align: center; color: Blue;'>&copy;This app is built using Streamlit and Python ~hussam</i>",
 unsafe_allow_html=True)
