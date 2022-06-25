import json

import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver


class FactorTrust:

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        #self.solver = CaptchaSolver()

    def submit(self, fname, mname, lname, email, ssn, phone, dob, address_line1, address_line2, zip, city,  state_abbreviation):

        r = self.session.get('https://lendprotect.transunion.com/Consumer/CreditFreeze/PersonInfo.aspx')
        soup = BeautifulSoup(r.text, 'html.parser')
        inputs = {i.get('name'): i.get('value') for i in soup.select('#form1 input')}
        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': inputs['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': inputs['__VIEWSTATEGENERATOR'],
            '__VIEWSTATEENCRYPTED': '',
            'ctl00$ContentPlaceHolder1$firstName': fname,
            'ctl00$ContentPlaceHolder1$mn': '',
            'ctl00$ContentPlaceHolder1$lastName': lname,
            'ctl00$ContentPlaceHolder1$emailInput': email,
            'ctl00$ContentPlaceHolder1$ssn': ssn,
            'ctl00$ContentPlaceHolder1$dob': dob.strftime('%Y-%m-%d'),
            'ctl00$ContentPlaceHolder1$address': address_line1,
            'ctl00$ContentPlaceHolder1$address2': '',
            'ctl00$ContentPlaceHolder1$city': city,
            'ctl00$ContentPlaceHolder1$state': state_abbreviation,
            'ctl00$ContentPlaceHolder1$zip': zip,
            'ctl00$ContentPlaceHolder1$livedThere': 'yes',
            'ctl00$ContentPlaceHolder1$prevAddress1': '',
            'ctl00$ContentPlaceHolder1$prevAddress2': '',
            'ctl00$ContentPlaceHolder1$prevCity': '',
            'ctl00$ContentPlaceHolder1$prevState': '',
            'ctl00$ContentPlaceHolder1$prevZip': '',
            'ctl00$ContentPlaceHolder1$Submit': 'Continue to verify identity',
        }

        r = self.session.post('https://lendprotect.transunion.com/Consumer/CreditFreeze/PersonInfo.aspx', data=data)
        soup = BeautifulSoup(r.text, 'html.parser')

        msg = ''
        try:
            # I don't know the success state
            if r.status_code == 200 and 'I do not know'.upper() in soup.select_one('title').text:
                msg = soup.select_one('.informational_padding > p').text
                print('=> Submitted Successfully!')
                return True, msg
            else:
                errors = soup.select_one('#ContentPlaceHolder1_valSumErrors').text.strip()
                if not errors:
                    errors = '\n'.join([e.text.strip() for e in soup.select('.error')])

                print('=> Failed to submit:', errors)
                return False, errors
        except Exception as e:
            print('ERROR:', e)
            print('=> EXCEPTION Failed to submit:', r.text)
            return False, msg


if __name__ == '__main__':
    FactorTrust().submit(fname='a', lname='b', email='df')


