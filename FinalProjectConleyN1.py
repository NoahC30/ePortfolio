# Noah Conley
# cit 383
# Final Project
import argparse

# sender pass hhehhsmdwhdzabmz

# things needed for this project to work
import paramiko, datetime, sys, getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Task 1

# login and find files method below
def findAndListFiles (ipaddr, uname, passwd):
    # utilize SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect using SSH
    ssh.connect(ipaddr, uname, passwd)

    # build a command to try and find files
    findcmd = 'find ~ -type f -mtime 14 -printf "%f\t%TY-%Tm-%Td %TH:%TM:TS\n"'

    # execute the find command
    stdin, stdout, stderr = ssh.exec_command(findcmd)

    # handle output
    results = []

    for line in stdout.readlines():
        filename, modtime = line.strip().split('\t')
        mod_datentime = datetime.datetime.strptime(modtime, '%Y-%m-%d %H:%M:%S')
        results.append((filename, mod_datentime))

    # close SSH
    ssh.close()

    return results


# ----------------------------------------------------------------------------------------------------------------------
# email method below
def sendEmail ():
    # gather data for email
    sender = input("Enter your (sender) email: ")
    emailpass = getpass.getpass(prompt="Please enter your email password and press enter: ") # hidden at entry
    recipient = input("Enter the email recipient: ")

    # set up email
    message = MIMEMultipart()
    message["Subject"] = "Compromised files from " + uname + "home directory: "
    message["From"] = sender
    message["To"] = recipient

    # build email body
    results = findAndListFiles(ipaddr, uname, passwd)
    body = "List of files modified in the last 14 days:\n"
    for filename, mod_time in results:
        body += f"{filename}\t{mod_time}\n"

    message.attach(MIMEText(body, 'plain'))

    # attach a file to email
    Attachment = results[0][0]
    with open(Attachment, 'rb') as fa:
        emailatt = MIMEApplication(fa.read(), _subtype='octet-stream')
        emailatt.add_header('Content-Disposition', 'attachment', filename=Attachment)
        message.attach(emailatt)

    # connect to server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, emailpass)
    server.sendmail(sender, recipient, message.as_string())
    server.quit()

    print("Email has been sent!")

# ----------------------------------------------------------------------------------------------------------------------
# utilize cmd line args
if len(sys.argv) < 4 or '--help' in sys.argv:
    print('Program run syntax: python scriptname.py ip_address username password')
    sys.exit()

ipaddr = sys.argv[1]
uname = sys.argv[2]
passwd = sys.argv[3]

parser = argparse.ArgumentParser
parser.add_argument('--help')

sendEmail()

# end of task 1
# ----------------------------------------------------------------------------------------------------------------------


# Task 2
