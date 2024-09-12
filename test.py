from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def get_smtp_settings():
    """
    Get the SMTP settings for sending emails using Zoho's SMTP server.
    """
    return ('smtp.zoho.com', 587, False)  # Zoho uses TLS on port 587



def send_email(subject, recipients):
    """
    Send an email using SMTP.
    """
    message = MIMEMultipart()
    message['From'] = f"Naqeeb <de.naqeeb@brbgroup.pk>"
    message['To'] = "de.kashan@brbgroup.pk" 
    message['Subject'] = subject
    
    message.attach(MIMEText("<h1>body</h1>", 'html'))

    smtp_server, port, use_ssl = get_smtp_settings()
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login("de.naqeeb@brbgroup.pk", "DeNaqeeb@321")
        server.sendmail("de.naqeeb@brbgroup.pk", recipients, message.as_string())
        server.quit()
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Failed to send email check if email and password is correct: {str(e)}"
    



print(send_email("testing new string method","de.laiba@brbgroup.pk"))