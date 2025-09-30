# import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_email(sender_email, sender_password, receiver_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    except Exception as e:
        # st.error(f"Error: {e}")
        return False

# # Streamlit UI
# st.title("📧 Send an Email")

# sender_email = st.text_input("Sender Email")
# sender_password = st.text_input("Sender Email Password", type="password")
# receiver_email = st.text_input("Receiver Email")
# subject = st.text_input("Subject")
# message = st.text_area("Message")

# if st.button("Send Email"):
#     if send_email(sender_email, sender_password, receiver_email, subject, message):
#         st.success("Email sent successfully!")
