import smtplib
from email.mime.text import MIMEText
from db_operations import add_user, log_message

def send_email(name, email, message):
    add_user(name, email)

    sender_email = "your_email@example.com"
    sender_password = "your_password"
    smtp_server = "smtp.example.com"
    smtp_port = 465

    msg = MIMEText(message)
    msg['Subject'] = 'Subject Here'
    msg['From'] = sender_email
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        print("Email sent successfully.")
        log_message(email, message)
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    # Test sending email
    send_email("Test User", "testuser@example.com", "This is a test message.")