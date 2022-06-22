import json

import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver


class Innovis:

    def __init__(self):
        self.session = requests.session()
        # self.session.headers = {
        #     'Host': 'innovis.com',
        #     'Origin': 'https://innovis.com',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'Referer': 'https://innovis.com/securityFreeze/register',
        #     'Accept-Language': 'en-US,en;q=0.9',
        # }
        #self.solver = CaptchaSolver()

    def submit(self, fname, mname, lname, email, ssn, phone, dob, address_line1, address_line2, zip, city,  state_abbreviation):

        data = {
            #'SYNCHRONIZER_TOKEN': token,
            'SYNCHRONIZER_URI': '/securityFreeze/register',
            'requestType': 'SFRZ-ADD',
            'tlDateFrom': '',
            'tlDateTo': '',
            'tlConfirmationNumber': '',
            'thirdPartyName': '',
            'tpDateFrom': '',
            'tpDateTo': '',
            'tpConfirmationNumber': '',
            'rlConfirmationNumber': '',
            'rmConfirmationNumber': '',
            'firstName': fname,
            'middleName': '',
            'lastName': lname,
            'generationCode': '',
            'phone': f'({phone[:3]}) {phone[3:6]}-{phone[6:]}',
            'ssn': f'{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}',
            'birthDate': dob.strftime('%m/%d/%Y'),
            'victim': 'N',
            'address': address_line1,
            'addressLine2': address_line2 or '',
            'city': city,
            'state': state_abbreviation,
            'zip': zip,
            'submit': 'submitSFForm',
        }
        #print(data)

        r = self.session.post('https://innovis.com/securityFreeze/register', data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.select_one('#SYNCHRONIZER_TOKEN').get('value')
        data['SYNCHRONIZER_TOKEN'] = token

        r = self.session.post('https://innovis.com/securityFreeze/register', data=data)
        soup = BeautifulSoup(r.text, 'html.parser')

        msg = ''
        try:
            if r.status_code == 200 and 'Confirmation'.upper() in soup.select_one('title').text:
                msg = soup.select_one('.informational_padding > p').text
                print('=> Submitted Successfully!')
                return True, msg
            else:
                errors = '\n'.join(soup.select('.error_message'))
                if errors:
                    msg = errors
                else:
                    msg = soup.select_one('div.thick_border_box h1').text

                print('=> Failed to submit:', msg)
                return False, msg
        except Exception as e:
            print('ERROR:', e)
            print('=> EXCEPTION Failed to submit:', r.text)
            return False, msg


if __name__ == '__main__':
    Innovis().submit(fname='a', lname='b', email='df')

