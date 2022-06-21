# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import codecs


session = requests.session()
session.headers = {
    'Host': 'www.chexsystems.com',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://www.chexsystems.com/web/chexsystems/consumerdebit/page/securityfreeze/placefreeze/!ut/p/z1/',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8,de;q=0.7',
}


url = 'https://www.chexsystems.com/web/chexsystems/consumerdebit/page/securityfreeze/placefreeze'
r = session.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
captcha_image = 'https://www.chexsystems.com' + soup.select_one('#captcha_image').get('src')
print(captcha_image)


post_url = 'https://www.chexsystems.com' + codecs.decode(r.text.split('FreezeForm.action="')[1].split('";')[0], encoding='unicode_escape')

print(post_url)
print(session.cookies)
input('?')


data = {
    'termsCondtn': 'agree',
    'ageVerify': 'yes',
    'firstName': 'Yixian',
    'middleName': '',
    'lastName': 'Li',
    'dobMon': '06',
    'dobDay': '20',
    'dobYear': '1987',
    'govtNbrPart1': '085',
    'govtNbrPart2': '98',
    'govtNbrPart3': '2518',
    'vrfyGovtNbrPart1': '085',
    'vrfyGovtNbrPart2': '98',
    'vrfyGovtNbrPart3': '2518',
    'driversLicense': '',
    'addrLine1': '21540 23rd Avenue',
    'addrLine2': '',
    'cityName': 'Bayside',
    'stateCode': 'NY',
    'postalCode': '11360',
    'areaCode': '',
    'phonePrefix': '',
    'phoneSuffix': '',
    'captchaText': 'mm3hd',
}

r = session.post(post_url, data=data)
soup = BeautifulSoup(r.text, 'html.parser')
errors = ' - '.join(soup.select('.panel-body[style*=red] li'))
print(r.text)
print(errors)