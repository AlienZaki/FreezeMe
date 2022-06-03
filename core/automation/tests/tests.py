from django.test import TestCase
from ..corelogic import Corelogic
from ...models import Client, State, Settings


class AutomationScriptsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Settings.objects.create(captcha_key='7e9ca143e7aa1d52071545be45efb5d5')
        state = State.objects.create(name='California', abbreviation='CA')
        Client.objects.create(
            fname="Alien",
            mname="",
            suffix="",
            lname="Zaki",
            city="Magic",
            state=state,
            zip="123456",
            address_line1="King street",
            address_line2=None,
            phone=None,
            email="test@domain.com",
            ssn="999999999",
            dob="1990-10-20",
            freeze_date="2022-05-08",
            id_card="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            passport="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            driver_license="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            residency="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
        )

    def setUp(self):
        self.client = Client.objects.get(ssn='999999999')

    def test_LexisNexis(self):
        pass

    def test_Corelogic(self):
        client = self.client
        r = Corelogic().submit(fname=client.fname, lname=client.lname, email=client.email)
        print(r)