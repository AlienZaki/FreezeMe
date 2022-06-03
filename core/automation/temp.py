import requests

data = {
   "reason[reason]":"CONSUMER",
   "reason[detailTitle]":"",
   "reason[detailAgency]":"",
   "reason[detailJuris]":"",
   "reason[detailRptNo]":"",
   "reason[detailDesc]":"",
   "reason[detailFile]":"",
   "reason[optinReason]":"",
   "contact[phone1]":"710",
   "contact[phone2]":"321",
   "contact[phone3]":"6541",
   "contact[email]":"test@domain.com",
   "contact[postal]":"-1",
   "subjects[0][nameFirst]":"Alien",
   "subjects[0][nameMiddle]":"",
   "subjects[0][nameLast]":"Zaki",
   "subjects[0][ssn1]":"999",
   "subjects[0][ssn2]":"99",
   "subjects[0][ssn3]":"9999",
   "subjects[0][abbreviate]":"Alien  Zaki",
   "addresses[0][addressLine1]":"King street",
   "addresses[0][addressLine2]":"",
   "addresses[0][addressCity]":"Magic",
   "addresses[0][addressState]":"CA",
   "addresses[0][addressZip]":"12345",
   "addresses[0][addressZip4]":"",
   "addresses[0][abbreviate]":"King street ... CA 123456"
}
print(data)
url = 'https://optout.lexisnexis.com/'
r = requests.post(url, data=data)
print(r.text)