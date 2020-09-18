#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
import argparse


#Set up parsing
parser = argparse.ArgumentParser(description='Emails a confirmation that VNC instance is created')
parser.add_argument('--netid', type=str, help='NetID')
parser.add_argument('--name', type=str, help='First Last')
parser.add_argument('--spec', type=str, help='u for unr.edu; n for nevada.unr.edu; e for whole email', default='n')
parser.add_argument('--email', type=str, help="Unique email")

#Send VNC Instance confirmation
def send_support(netid, name, spec, email=None):
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(2)
    smtp.connect('smtp.unr.edu')
    
    msg = EmailMessage()
    msg['Subject'] = f'Linux Remote Instance Request: {netid}'
    msg['From'] = 'vpham@unr.edu'
    if spec is 'n':
        msg['To'] = (f'{netid}@nevada.unr.edu', 'ehelp@engr.unr.edu')
    elif spec is 'u':
        msg['To'] = (f'{netid}@unr.edu', 'ehelp@engr.unr.edu')
    elif spec is 'e':
        if email is None:
            smtp.quit()
            logging.warning("No Emailed specified but spec='e'")
            return
        msg['To'] = (email, 'ehelp@engr.unr.edu')
    else:
        return
    msg['CC'] = 'ehelp@engr.unr.edu'

    msg.set_content(f"""\
    Hello {name},
        
        I have set up a new Linux instance for you. You should be able to log in now at https://remote.engr.unr.edu. Please let me know if you have any problems.
        
        Here is also a quick guide on getting started if you're unfamiliar: https://ph.engr.unr.edu/w/remote-instance-help/

    Vincent Pham
    Engineering Computing
    University of Nevada, Reno
    vpham@unr.edu
    """)

    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    
    smtp.sendmail(msg['From'], msg['CC'], msg.as_string())
    
    smtp.quit()

    print(msg.as_string())
    print(f"\n\nSent to {netid}.")

#Main
if __name__ == '__main__':
    args = parser.parse_args()
    send_support(args.netid, args.name, args.spec, args.email)

