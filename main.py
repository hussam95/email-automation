"""https://www.geeksforgeeks.org/how-to-send-automated-email-messages-in-python/"""

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from secrets import choice
import smtplib
import os
import getpass
import streamlit as st
from PIL import Image 
import pandas as pd

# Landing Page Image Loading
img = Image.open(r"C:\Users\Hussam\Desktop\email_automation\zem dash header public view.jpg")

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
send_email = st.button("Send Email")

# Email Data Connection
email_data  = pd.read_csv(r"\Users\Hussam\Desktop\email_automation\email_record_ZEM.csv")

# Sifitng Email dataframe w.r.t user selection 
if choice == "Finance and Accounts":
    recipients = email_data[email_data["Deparment"]=="Finance and Accounts"]["Email"].to_list()
elif choice == "Audit Compliance":
    recipients = email_data[email_data["Deparment"]=="Audit Compliance"]["Email"].to_list()
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

# Main 
if send_email==True:
    try:
        password = sender_pass
        smtp = smtplib.SMTP('mail.zembuilders.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_sender, password)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg.attach(MIMEText(email_content))

        to = recipients 
        smtp.sendmail(from_addr=email_sender,
        to_addrs=to, msg=msg.as_string())
        smtp.quit()
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
st.markdown("<i style='text-align: center; color: Blue;'>&copy;This app is built using Streamlit and Python ~hussam</i>", unsafe_allow_html=True)