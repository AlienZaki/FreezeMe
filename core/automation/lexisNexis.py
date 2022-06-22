import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver


class LexisNexis:

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'authority': 'optout.lexisnexis.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://optout.lexisnexis.com',
            'referer': 'https://optout.lexisnexis.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.solver = CaptchaSolver()

    def submit(self, fname, mname, lname, email, ssn, phone, address_line1, address_line2, zip, city,  state_abbreviation):
        url = 'https://optout.lexisnexis.com/'
        # r = self.session.get(url)
        # soup = BeautifulSoup(r.text, 'html.parser')

        # try:
        #     token = self.solver.solve_recaptcha(site_key='6Ld9w2wUAAAAAOO1row7acswabxRGqzE1J40ww7E', url=url)['code']
        # except Exception as e:
        #     raise Exception(e)

        data = {
            'reason[reason]': 'CONSUMER',
            'reason[detailTitle]': '',
            'reason[detailAgency]': '',
            'reason[detailJuris]': '',
            'reason[detailRptNo]': '',
            'reason[detailDesc]': '',
            'reason[detailFile]': '',
            'reason[optinReason]': '',
            'contact[phone1]': phone[:3],
            'contact[phone2]': phone[3:6],
            'contact[phone3]': phone[6:],
            'contact[email]': email,
            'contact[postal]': '-1',
            'subjects[0][nameFirst]': fname,
            'subjects[0][nameMiddle]': mname,
            'subjects[0][nameLast]': lname,
            'subjects[0][ssn1]': ssn[:3],
            'subjects[0][ssn2]': ssn[3:5],
            'subjects[0][ssn3]': ssn[5:],
            'subjects[0][abbreviate]': f'{fname} {mname or ""} {lname}',
            'addresses[0][addressLine1]': address_line1 or '',
            'addresses[0][addressLine2]': address_line2 or '',
            'addresses[0][addressCity]': city,
            'addresses[0][addressState]': state_abbreviation,
            'addresses[0][addressZip]': zip[:5] or '',
            'addresses[0][addressZip4]': '',
            'addresses[0][abbreviate]': f'{address_line1} ... {state_abbreviation} {zip}',
        }
        print(data)
        r = self.session.post(url, data=data)

        msg = ''
        try:
            if r.status_code == 200 and r.json()['status'] == 0:
                msg = f'Confirmation {r.json()["data"][0]}'
                print('=> Submitted Successfully!')
                return True, msg
            else:
                msg = '\n'.join(r.json()["data"])
                print('=> Failed to submit:', r.text)
                return False, msg
        except Exception:
            print('=> Failed to submit:', msg)
            return False, msg


if __name__ == '__main__':
    LexisNexis().submit(fname='a', lname='b', email='df')

