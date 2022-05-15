import requests
from bs4 import BeautifulSoup


class Corelogic:

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'authority': 'teletrackfreeze.corelogic.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        }

    def submit(self, fname, lname, email):
        url = 'https://teletrackfreeze.corelogic.com/'
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': soup.select_one('#__VIEWSTATE').get('value'),
            '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR').get('value'),
            '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION').get('value'),
            'ctl00$cphLeftColumn$ctl00$txtFirstName': fname,
            'ctl00$cphLeftColumn$ctl00$txtLastName': lname,
            'ctl00$cphLeftColumn$ctl00$txtEmail': email,
            'ctl00$cphLeftColumn$ctl00$txtEmailConfirm': email,
            'ctl00$cphLeftColumn$ctl00$rblFreezeType': '1',
            'g-recaptcha-response': '',
            'ctl00$cphLeftColumn$ctl00$btnSubmit': 'Submit',
        }
        print(data)


if __name__ == '__main__':
    Corelogic().submit(fname='a', lname='b', email='df')