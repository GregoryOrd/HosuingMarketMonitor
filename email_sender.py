import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def generate_changes_summary(changes):
    if len(changes) <= 0:
        return ""
        
    old = changes[0]
    new = changes[1]

    summary = ""
    for a in changes:
        summary = summary + f"- ${old.price} changed to ${new.price} for {a.beds} beds, {a.baths} baths, {a.town}, {a.addr}, {a.url}\n\n"
    return summary

def generate_summary(additions):
    summary = ""
    for a in additions:
        summary = summary + f"- ${a.price}, {a.beds} beds, {a.baths} baths, {a.town}, {a.addr}, {a.url}\n\n"
    return summary

def sendEmail(deletions, additions, price_changes, min_price, max_price):
    file_path = "~/.retriever_creds"
    full_path = os.path.expanduser(file_path)

    lines = []
    with open(full_path, "r") as f:
        for line in f:
            lines.append(line)

    # Email account credentials
    sender_email = lines[0]
    receiver_email = lines[1].strip()
    cc_email = lines[2].strip()
    password = lines[3] 

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = cc_email
    message["Subject"] = "Real Estate Market Update"

    # Email body
    body = f"""Hello,

This is a real estate listings update for listings matching your criteria (min price: ${min_price}, max_price: ${max_price}) in Central Saanich/Sidney on ReMax.

- {len(price_changes)} listing(s) have seen price changes
- {len(additions)} new listing(s) have been added.
- {len(deletions)} listing(s) have been removed.

Here is a summary of the price changes:
{generate_changes_summary(price_changes)}

Here is a summary of the additions:

{generate_summary(additions)}

Here is a summary of the deletions:

{generate_summary(deletions)}

Regards,
Your Market Updates Team
"""
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail's SMTP server and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.sendmail(sender_email, cc_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()
