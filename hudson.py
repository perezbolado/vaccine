
from lxml import html
import requests

class HudsonCounty():
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = 'https://hudsoncovidvax.org'

    def getstatus(self)->bool:
        response = self.session.get(self.base_url + '/login')
        tree = html.fromstring(response.content)
        token = tree.xpath('//meta[@name="csrf-token"]')[0].get('content')
        response = self.session.post(self.base_url  + '/login',data={'_token': token, 'email': self.username, 'password': self.password})
        response = self.session.send(response.request)
        tree = html.fromstring(response.content)
        appt_link = tree.xpath('//a[text()="Schedule Appointment"]/@href')[0]
        response = self.session.get(appt_link)
        result = response.text.find('IF YOU ARE SEEING THIS MESSAGE, IT MEANS THAT WE ARE NOT ABLE TO SCHEDULE ANY ADDITIONAL APPOINTMENT REQUESTS AT THIS TIME')
        response = self.session.post(self.base_url + '/logout',data={'_token': token } )
        return result == -1

