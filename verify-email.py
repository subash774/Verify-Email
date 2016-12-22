import re # Regex imported to validate email address
import dns.resolver # No inbuilt DNS check system so you've to import
import socket
import smtplib # SMTP library to be imported to check if host has SMTP server

# Address used for SMTP MAIL FROM command
from_address = "sample@email.com"

# Regex for email syntax/format
regex = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"


while True:
    email_input = input("Please enter the email address to verify:")
    email = str(email_input)

    # Syntax check - Validate the email address to make sure it matchs the pattern
    match = re.match(regex, email)
    if match == None:
        print("Email you entered doesn't follow the normal pattern, please try again! \n \n")
        continue


    # split the address after @ sign so we can get the domain
    domain = email.split("@")
    domain = str(domain[1])
    print("Domain:", domain)

    # look for MX record, see if SMTP exists on hosts side
    records = dns.resolver.query(domain, "MX") # Returns multiple data in form of list if wanted
    mx_record = records[0].exchange # the first (the only in this case) email / mx record
    mx_record = str(mx_record)

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mx_record)
    server.helo(host)
    server.mail(from_address)
    code, message = server.rcpt(str(email)) # Tuple
    server.quit()


    # If returned 250, email exists, if normally 550, it doesn't exist
    if code == 250:
        print("The email exists! \n \n")
    else:
        print("Some email clients don't really co-operate so can't be 100% certain but doesn't seem like this email exists, sorry \n \n")
