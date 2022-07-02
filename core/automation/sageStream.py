import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver
import json


class SageStream:

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'authority': 'submit.api.sagestreamllc.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        #self.solver = CaptchaSolver()

    def submit(self, fname, mname, lname, email, ssn, phone, dob, address_line1, address_line2, zip, city,  state_abbreviation):
        data = {
            "type": "Security Freeze",
            "consumer": "self",
            "self": {
                "identity": {
                    "firstName": fname,
                    "lastName": lname,
                    "dob": dob.strftime('%Y-%m-%d'),
                    "ssn": f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}",
                    "email": email,
                    "addressLine1": address_line1,
                    "city": city,
                    "state": state_abbreviation,
                    "stateofresidence": state_abbreviation,
                    "zip": zip
                },
            "documents": {
                "option": 0,
                "files": [
                    {"bucket": "sagestream-file-api-prod", "key": "e7082666-c5cd-41b2-9447-018f1c445f8f/self-0.png"}
                ]}
            }, "parameters": {"recover": False}
        }

        r = self.session.post('https://submit.api.sagestreamllc.com/forms', data=json.dumps(data))
        msg = ''
        try:
            if r.status_code == 201:
                print('=> Submitted Successfully!')
                msg = 'Your request has been successfully submitted'
                return True, msg
            else:
                print('=> Failed to submit:', msg)
                error = r.text
                return False, error
        except Exception:
            print('=> Failed to submit:', msg)
            return False, msg


if __name__ == '__main__':
    SageStream().submit(fname='a', lname='b', email='df')


