
from email.mime.multipart import MIMEMultipart
import datetime
from os import times
import sys
import smtplib, ssl
import configparser
import time
import hudson

class Alerter:
    def __init__( self, filename:str ):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.smtp_port = self.config['mail']['port']
        self.smtp_password = self.config['mail']['password']
        self.smtp_sender = self.config['mail']['sender']
        self.smtp_server = self.config['mail']['smtp_server']
        self.email_recepients = self.config['mail']['recipients']
        self.sites = { 
                'hudsoncovidvax.org' : hudson.HudsonCounty(self.config['hudsoncovidvax.org']['username'], self.config['hudsoncovidvax.org']['password'])
        }
        self.frequency = self.config['alerter']['frequency']

    def send_email(self, message:str):
        server = smtplib.SMTP(self.smtp_server,587)
        server.starttls()
        server.login(self.smtp_sender,self.smtp_password)
        for email in self.email_recepients.split(','):
            msg = MIMEMultipart()
            msg['From'] = self.smtp_sender
            msg['To'] = email
            msg['Subject'] = message
            server.sendmail(self.smtp_sender,email,message)
        server.quit()

    def server_loop(self):
        while True:
            for name,vaccine_site in self.sites.items():
                print('Checking: {}'.format(name))
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                print ("Checking for vaccines on {} @ {}".format(name, timestamp))
                try:
                    if(vaccine_site.getstatus()):
                        print ("Vaccines available!!! Sending Email")
                        self.send_email('Vaccine Available:{} @ {}'.format(name, timestamp))
                    else:
                        print ("No vaccines available yet")
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    
            print('Sleeping for: {} minutes\n'.format(self.frequency))
            time.sleep(int(self.frequency)*60)

if __name__ == "__main__":
    # execute only if run as a script
    a = Alerter('settings.ini')
    a.server_loop()