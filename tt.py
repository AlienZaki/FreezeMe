import requests
from bs4 import BeautifulSoup

session = requests.session()

headers = {
    'Host': 'innovis.com',
    'Origin': 'https://innovis.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://innovis.com/securityFreeze/register',
    'Accept-Language': 'en-US,en;q=0.9',

}

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
    'firstName': 'Yixian',
    'middleName': '',
    'lastName': 'Li',
    'generationCode': '',
    'phone': '(718) 353-0225',
    'ssn': '654-98-7132',
    'birthDate': '06/20/1987',
    'victim': 'N',
    'address': '21540 23rd Avenue',
    'addressLine2': '',
    'city': 'Bayside',
    'state': 'NY',
    'zip': '11360',
    'submit': 'submitSFForm',
}

r = session.post('https://innovis.com/securityFreeze/register', data=data)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.select_one('title').text)

url = 'https://innovis.com/securityFreeze/index'
r = session.get(url)
print(session.cookies['JSESSIONID'])

token = soup.select_one('#SYNCHRONIZER_TOKEN').get('value')
data['SYNCHRONIZER_TOKEN'] = token
r = session.post('https://innovis.com/securityFreeze/register', data=data)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.select_one('title').text)