import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver


class Corelogic:

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'authority': 'teletrackfreeze.corelogic.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        }
        self.solver = CaptchaSolver()

    def submit(self, fname, lname, email):
        url = 'https://teletrackfreeze.corelogic.com/'
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            token = self.solver.solve_recaptcha(site_key='6Ld9w2wUAAAAAOO1row7acswabxRGqzE1J40ww7E', url=url)['code']
        except Exception as e:
            raise Exception(e)

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
            'g-recaptcha-response': token,
            'ctl00$cphLeftColumn$ctl00$btnSubmit': 'Submit',
        }
        print(data)
        r = self.session.post(url, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        msg = ''
        try:
            msg = soup.select_one('#cphLeftColumn_ctl00_pnlConfirmationFreeze').text.strip()
            if 'Thank you for submitting your request' in msg:
                print('=> Submitted Successfully!')
                return True, msg
            else:
                print('=> Failed to submit:', msg)
                return False, msg
        except Exception:
            print('=> Failed to submit:', msg)
            return False, msg


if __name__ == '__main__':
    Corelogic().submit(fname='a', lname='b', email='df')