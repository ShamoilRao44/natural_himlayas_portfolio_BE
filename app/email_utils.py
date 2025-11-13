import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject: str, body: str, to: str):
    from_email = EMAIL_ADDRESS  # Replace with your email
    from_password = EMAIL_PASSWORD  # Replace with your generated App Password

    print(f"EMAIL_ADDRESS: {from_email}")
    print(f"EMAIL_PASSWORD: {from_password}")
    
    # Create the email headers
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to
    message["Subject"] = subject

    # Attach the email body
    message.attach(MIMEText(body, "plain"))

    # Connect to the Gmail server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, from_password)

    # Send the email
    server.send_message(message)
    server.quit()
