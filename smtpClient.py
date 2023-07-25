import smtplib

def Feedback(sender_email, sender_password):
    # Set up connection to email server
    smtp_server = "sandbox.smtp.mailtrap.io"
    smtp_port = 587
    sender_email="78e3f1f01985b4"
    sender_password="7223dd08913c4f"

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)

        # Compose the email message
        subject = input("> Subject:  ")
        body = input("> Message:  ")
        recipient_email = "78e3f1f01985b4"
        message = f"Subject: {subject}\n\n{body}"

        # Send the email
        smtp.sendmail(sender_email, recipient_email, message)
        
        print("Email sent successfully!")
