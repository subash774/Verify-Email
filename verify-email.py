import re # Regex imported to validate email address
import dns.resolver # No inbuilt DNS check system so you've to import
import socket
import smtplib

while True: # Infinite loop
    email = str(input("Enter the email address you want to verify: \n")) # For user to input the email
    # Validate the email address to make sure it matchs the pattern
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        print("Email you entered doesn't follow the normal pattern, please try again!")
        continue # Runs the loop again without running anything below

    emails = dns.resolver.query(email, "MX") # Returns a list / array
    mx = str(emails[0]) # Select the first email (the only one in our case)

    host = socket.gethostname()
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    # "check_mx" checks if the host has SMTP Server, use "check_mx" if you only want to know if SMTP exists "verify" checks if the host has SMTP Server and the email really exists
    server.connect(mx)
    server.helo(host)
    server.mail(mail)
    code, message = server.rcpt(mail)
    server.quit()
    if code == 250:
        print("The email exists!")
    else:
        print("Some email clients don't really co-operate so can't be 100% certain but doesn't seem like this email exists, sorry")
