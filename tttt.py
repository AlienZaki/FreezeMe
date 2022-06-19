import requests
from bs4 import BeautifulSoup

session = requests.session()
session.headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.chexsystems.com',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-gpc': '1',
}
r = session.get('https://www.chexsystems.com/web/chexsystems/consumerdebit/page/securityfreeze/placefreeze')
post_url = r.url
session.headers['Referer'] = post_url
soup = BeautifulSoup(r.text, 'html.parser')
captcha_image = 'https://www.chexsystems.com' + soup.select_one('#captcha_image').get('src')
print(captcha_image)
captcha = input('captcha:\n')


data = {
    'termsCondtn': 'agree',
    'ageVerify': 'yes',
    'firstName': 'McKenzie',
    'middleName': '',
    'lastName': 'Adams',
    'dobMon': '10',
    'dobDay': '28',
    'dobYear': '1977',
    'govtNbrPart1': '098',
    'govtNbrPart2': '55',
    'govtNbrPart3': '5678',
    'vrfyGovtNbrPart1': '098',
    'vrfyGovtNbrPart2': '55',
    'vrfyGovtNbrPart3': '5678',
    'driversLicense': '',
    'addrLine1': '7710 Balboa Ave Ste 313',
    'addrLine2': '',
    'cityName': 'San Diego',
    'stateCode': 'CA',
    'postalCode': '92111',
    'areaCode': '701',
    'phonePrefix': '732',
    'phoneSuffix': '0037',
    'captchaText': captcha,
}
response = session.post(post_url, data=data)

print(response.text, response.status_code)
