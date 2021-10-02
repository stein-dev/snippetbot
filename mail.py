import smtplib, ssl

def send_email(message):
    try:
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "snippet.media.mail@gmail.com"
        receiver_email = "test@gmail.com"
        password = "test"

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except ValueError as e:
        print(e)  

def get_msg():
    try:
        f = open("transaction.txt", "r")
        tr = str(f.read())
        msg = "\r\n".join([
                    "From: snippet.media.mail@gmail.com",
                    "To: test.012@gmail.com",
                    "Subject: Redeem Notification",
                    "",
                    tr
                    ])
        return msg
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()      

send_email(get_msg())




          
