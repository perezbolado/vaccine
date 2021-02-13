
from email import message
import sys,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime,time
import hudson

class Alerter:
    def __init__( self ):
        # Get environment variables
        self.smtp_port          = os.getenv('SMTP_PORT')
        self.smtp_password      = os.getenv('SMTP_PASSWORD')
        self.smtp_sender        = os.getenv('SMTP_EMAIL')
        self.smtp_server        = os.getenv('SMTP_SERVER')
        self.email_recipients   = os.getenv('EMAIL_RECIPIENTS')
        self.frequency          = os.getenv('ALERT_FREQUENCY')
        self.sites = { 
                'hudsoncovidvax.org' : hudson.HudsonCounty(os.getenv('HUDSON_USER'), os.environ.get('HUDSON_PASS'))
        }
        print('Start Alerter. Will check every: {} minutes'.format(self.frequency))
                
    def send_email(self, subject:str, message:str='' ):
        server = smtplib.SMTP(self.smtp_server,587)
        server.starttls()
        server.login(self.smtp_sender,self.smtp_password)
        for email in self.email_recipients.split(','):
            msg = MIMEMultipart()
            msg['From'] = self.smtp_sender
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, "plain"))
            server.sendmail(self.smtp_sender,email,msg.as_string())
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
                        subject = 'Vaccine Available:{} @ {}'.format(name, timestamp)
                        message = 'Hurry Vacines are available @ {}'.format(name)
                        self.send_email(subject, message)
                    else:
                        print ("No vaccines available yet")
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    
            print('Sleeping for: {} minutes\n'.format(self.frequency))
            time.sleep(int(self.frequency)*60)

if __name__ == "__main__":
    a = Alerter()
    a.server_loop()