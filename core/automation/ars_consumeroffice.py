import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FreezeMe.settings")
django.setup()
from settings.models import Settings
from captcha import CaptchaSolver
import requests, json
from twocaptcha import TwoCaptcha



class ARS:

    def __init__(self):
        self.session = requests.session()
        self.session.get('https://www.ars-consumeroffice.com/add')
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        self.session.headers['x-xsrf-token'] = self.session.cookies['XSRF-TOKEN']

    def upload(self):

        payload = {'sessionId': '588ae00e-f41e-7b17-24bb-b3100a2db5b5'}
        files = [
            ('file', open('C:/Users/alien/Pictures/11.png', 'rb'))
        ]
        url = "https://www.ars-consumeroffice.com/api/v1/security-freeze/upload"
        response = self.session.post(url, data=payload, files=files)

        print(response.text)

    def submit(self):
        twocaptcha_key = Settings.objects.get(name='2captcha_key').value
        solver = TwoCaptcha(twocaptcha_key)
        balance = solver.balance()
        print(balance)
        res = solver.recaptcha(sitekey='6Le3QaAaAAAAAF0IJ3ZjNtvscMqPwGLYYFWtYio_', url='https://www.ars-consumeroffice.com/add')
        print(res['code'])



        payload = json.dumps({
            "sessionId": "e8633160-0993-be15-ac4d-7e9b5215f7ef",
            "consumerInformation": {
                "firstName": "Alien",
                "middleInitial": None,
                "lastName": "Zaki",
                "suffix": "Zak",
                "city": "NEW CASTLE",
                "state": "AZ",
                "zipCode": "19720",
                "phoneNumber": "3026893120",
                "emailAddress": "eng.3bdo2020@gmail.com",
                "ssn": "000000000",
                "addressLines": [
                    "15 BOULDEN CIR",
                    "FF524-781 FISHISFASTD"
                ]
            },
            "documents": {
                "identificationDocuments": [
                    {
                        "originalName": "generate_voucher.PNG",
                        "generatedName": "ba8e917a-d876-4af2-8219-22301545ef6c.png"
                    }
                ],
                "proofsOfResidency": [],
                "additionalDocuments": []
            },
            "review": {
                "captcha": "03AGdBq25nEvkR1YWFsAIZrH-J8JNQK5HlhSAQ0tMs3M1RWcF0fZsdQQf5X-FgOeSHbpV07PN1IMa5xXOx9HhlUTewYhj-0XW3np-Wh30QtSYaTuw0l-whXgAdUj7kdPtUuCHtBF0j8yJPOK_ZIqIu3wJ2htnlhi6fpdLRNc9_IwVvTHKb8mAJQgtkmQDEAQWFiln0lw5KGskhbX3kC7mOBatGs6obMmE_sYgJfZ5KAwfMLl15MRyPyYfCLluKslvOPrloiKB7wran1ga97iYzMlFToelo-JWAReoWEGlIpvbdH5pqB5XHW1q7cFrmPNaZ67w8boU3gbsWGlR6Oj-bFsakmO5g0vOqhdOe-JiBbnOwPTf2bWoZPRLmnch0PxRodbt2Pr6X8BV1BECM_CPyNan6r3ff45O8HPP_tf0G2r2PU_a1j11Jf1lKm6TuVOln7UnBzNhyet_xDzJOgao13Hh4zPOPIJzPhA",
                "agreement": True
            },
            "action": "ADD",
            "actionStartDate": "2022-05-07"
        })
        self.session.headers['content-type'] = 'application/json'
        url = "https://www.ars-consumeroffice.com/api/v1/security-freeze"
        response = self.session.post(url, data=payload)
        print(response.text)
        return response.text


if __name__ == '__main__':
    ars = ARS()
    ars.upload()