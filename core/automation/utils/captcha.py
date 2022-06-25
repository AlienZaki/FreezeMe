import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FreezeMe.settings")
django.setup()

from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException
from core.models import Settings


class CaptchaSolver:

    def __init__(self):
        api_key = Settings.objects.first().captcha_key
        #api_key = '7e9ca143e7aa1d52071545be45efb5d5'
        self.solver = TwoCaptcha(api_key)

    def solve_recaptcha(self, site_key, url):
        try:
            print('=> Solving captcha...')
            result = self.solver.recaptcha(sitekey=site_key, url=url)
            print('=> Captcha solved!')
        except ApiException as e:
            errors = {
                'ERROR_BAD_PARAMETERS': '2Captcha: Please check the API key permissions',
                'ERROR_WRONG_USER_KEY': '2Captcha: Invalid Key',
                'ERROR_CAPTCHA_UNSOLVABLE': '2Captcha: Invalid site URL',
                'ERROR_WRONG_GOOGLEKEY': '2Captcha: Wrong google site key',
            }
            raise Exception(errors[e.__str__()])
        return result

    def solve_normal_captcha(self, image_url):
        try:
            print('=> Solving captcha...')
            result = self.solver.normal(image_url)
            print('=> Captcha solved!')
        except ApiException as e:
            errors = {
                'ERROR_BAD_PARAMETERS': '2Captcha: Please check the API key permissions',
                'ERROR_WRONG_USER_KEY': '2Captcha: Invalid Key',
                'ERROR_CAPTCHA_UNSOLVABLE': '2Captcha: Invalid site URL',
                'ERROR_WRONG_GOOGLEKEY': '2Captcha: Wrong google site key',
            }
            raise Exception(errors[e.__str__()])
        return result


if __name__ == '__main__':
    c = CaptchaSolver()
    #code = c.solve_normal_captcha('https://www.chexsystems.com/web/PA_ChexSystemsDotCom/CaptchaLoads.gif?1655817259651')['code']
    code = c.solve_recaptcha(site_key='6LdHJZoUAAAAANmKyn_5fJ1UeXrXrrcnUhLRIN_Y', url='https://consumers.clarityservices.com/idv?type=PLACE_SECURITY_FREEZE')
    print(code)
    import requests
    import json

    url = "https://consumersupport.clarityservices.com/api/v1/create_status_request"

    payload = json.dumps({
        "type": "PLACE_SECURITY_FREEZE",
        "ssn": "666464564",
        "name": {
            "first": "aasdasd",
            "middle": "",
            "last": "sfsdf",
            "generation": ""
        },
        "dob": "1986-12-31T22:00:00.000Z",
        "phone": "",
        "email": "asddasd@sdfsdfdsf.df",
        "address": {
            "street1": "21540 23rd Ave",
            "street2": None,
            "city": "Bayside",
            "state": "NY",
            "postal_code": "11360"
        },
        "pin": "",
        "representing_minor": "",
        "start_date": "2022-06-23T10:00:00.000Z",
        "end_date": "2022-06-24T10:00:00.000Z",
        "recaptchaResponse": code
    })
    headers = {
        'authority': 'consumersupport.clarityservices.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8,de;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'datatype': 'json',
        'origin': 'https://consumers.clarityservices.com',
        'pragma': 'no-cache',
        'referer': 'https://consumers.clarityservices.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Cookie': 'incap_ses_1099_2076957=ndbFP1rAEmXP08FcXm9AD0aBtGIAAAAAynROH+JP3ruBV5hvTHsq+w==; incap_ses_477_2076957=CC6cesJDflH8HQCqp6WeBvB/tGIAAAAAIL1jjwFNmUsPFhB6RA6f0w==; nlbi_2076957=Z30NOGIIoFuv1qn5ZkNnawAAAAAdp/cCtRNScW16K/PL+BR9; visid_incap_2076957=2Phoy2acSMOCzjWaN/8qkvB/tGIAAAAAQUIPAAAAAABL8vs7VLsMCzVEPR53rYNT; AWSALB=5JSKB+5lJwohPuaonlqHvKm/T4WfQmc7izbKYCHnHcmCz6OzgPShVfNUSf3sYxGnTlpmem5T5e7fjIg+fx2UjEAnTAXlqkKFugRmbfPot7bB7Vp4z6cvbqiQ+Ypp; AWSALBCORS=5JSKB+5lJwohPuaonlqHvKm/T4WfQmc7izbKYCHnHcmCz6OzgPShVfNUSf3sYxGnTlpmem5T5e7fjIg+fx2UjEAnTAXlqkKFugRmbfPot7bB7Vp4z6cvbqiQ+Ypp'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
