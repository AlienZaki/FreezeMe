import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FreezeMe.settings")
django.setup()
from core.models import Settings
import requests, json
from .utils.captcha import CaptchaSolver
from datetime import date
from urllib.parse import urlparse



class ARS:

    def __init__(self):
        self.session = requests.session()
        self.session.get('https://www.ars-consumeroffice.com/add')
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        self.session.headers['x-xsrf-token'] = self.session.cookies['XSRF-TOKEN']

        self.solver = CaptchaSolver()

    def upload(self, file_url):
        file_url = str(file_url)
        file_name = file_url.split('/')[-1].split('?')[0]
        print(file_name)
        r = requests.get(file_url, allow_redirects=True)
        open(f'temp/{file_name}', 'wb').write(r.content)

        payload = {'sessionId': '588ae00e-f41e-7b17-24bb-b3100a2db5b5'}
        files = [
            ('file', open(f'temp/{file_name}', 'rb'))
        ]
        url = "https://www.ars-consumeroffice.com/api/v1/security-freeze/upload"
        response = self.session.post(url, data=payload, files=files)
        print(response.text)

        #os.remove(f'temp/{file_name}')

        return (file_name, response.json()['generatedName'])

    def submit(self, fname, lname, email, ssn, phone, address_line1, address_line2, zip, city,  state_abbreviation, id_card, passport=None, driver_license=None, mname=None):
        """
            Upload attachments
        """
        if id_card:
            id_card_original, id_card_generated = self.upload(id_card)
        elif passport:
            passport_original, passport_generated = self.upload(passport)

        elif driver_license:
            driver_license_original, driver_license_generated = self.upload(driver_license)


        if id_card_generated or passport_generated or driver_license_generated:
            """
                Google Recaptcha Solver
            """
            try:
                url = 'https://www.ars-consumeroffice.com/add'
                token = self.solver.solve_recaptcha(site_key='6Le3QaAaAAAAAF0IJ3ZjNtvscMqPwGLYYFWtYio_', url=url)['code']
                input(token)
            except Exception as e:
                raise Exception(e)

            """
                Payload
            """
            payload = json.dumps({
                "sessionId": "588ae00e-f41e-7b17-24bb-b3100a2db5b5",
                "consumerInformation": {
                    "firstName": fname,
                    "middleInitial": mname,
                    "lastName": lname,
                    "suffix": None,
                    "city": city,
                    "state": state_abbreviation,
                    "zipCode": zip,
                    "phoneNumber": phone,
                    "emailAddress": email,
                    "ssn": ssn,
                    "addressLines": [
                        address_line1,
                        #address_line2 or ''
                    ]
                },
                "documents": {
                    "identificationDocuments": [
                        {
                            "originalName": id_card_original or passport_original or driver_license_original,
                            "generatedName": id_card_generated or passport_generated or driver_license_generated
                        }
                    ],
                    "proofsOfResidency": [],
                    "additionalDocuments": []
                },
                "review": {
                    "captcha": token,
                    "agreement": True
                },
                "action": "ADD",
                "actionStartDate": date.today().strftime('%Y-%m-%d')
            })
            print(payload)
            self.session.headers['content-type'] = 'application/json'
            url = "https://www.ars-consumeroffice.com/api/v1/security-freeze"
            response = self.session.post(url, data=payload)
            print(response.text)
            return response.text


if __name__ == '__main__':
    ars = ARS()
