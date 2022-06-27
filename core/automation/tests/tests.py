from django.test import TestCase
from ...models import Client, State, Settings
from ..corelogic import Corelogic
from ..lexisNexis import LexisNexis
from ..ars_consumeroffice import ARS
from ..innovis import Innovis
from ..chexsystems import Chexsystems
from ..telecomUtilityExchange import TelecomUtilityExchange
from ..factorTrust import FactorTrust
from ..clarityServices import ClarityServices


class AutomationScriptsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Settings.objects.create(captcha_key='7e9ca143e7aa1d52071545be45efb5d5')
        state = State.objects.create(name='New York', abbreviation='NY')
        Client.objects.create(
            fname="Yixian",
            mname="",
            suffix="",
            lname="Lu",
            city="Bayside",
            state=state,
            zip="11360",
            address_line1="21540 23rd Avenue",
            address_line2=None,
            phone='7103216541',
            email="eng.3bdo2020@gmail.com",
            ssn="085980518",
            dob="1987-07-20",
            freeze_date="2022-06-21",
            id_card="https://nyc3.digitaloceanspaces.com/freeze-me-space/media/uploads/Driver/driver_546970825.pdf",
            passport="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            driver_license="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            residency="https://www.google.com.eg/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
        )

    def setUp(self):
        self.client = Client.objects.get(ssn='085980518')

    def test_ClarityServices(self):
        client = self.client
        res = ClarityServices().submit(
            fname=client.fname,
            mname=client.mname,
            lname=client.lname,
            email=client.email,
            phone=client.phone,
            ssn=client.ssn,
            address_line1=client.address_line1,
            address_line2=client.address_line2,
            zip=client.zip,
            city=client.city,
            state_abbreviation=client.state.abbreviation,
            dob=client.dob,
        )
        print(res)

    # def test_TelecomUtilityExchange(self):
    #     client = self.client
    #     res = FactorTrust().submit(
    #         fname=client.fname,
    #         mname=client.mname,
    #         lname=client.lname,
    #         email=client.email,
    #         phone=client.phone,
    #         ssn=client.ssn,
    #         address_line1=client.address_line1,
    #         address_line2=client.address_line2,
    #         zip=client.zip,
    #         city=client.city,
    #         state_abbreviation=client.state.abbreviation,
    #         dob=client.dob,
    #     )
    #     print(res)

    # def test_TelecomUtilityExchange(self):
    #     client = self.client
    #     res = TelecomUtilityExchange().submit(
    #         fname=client.fname,
    #         mname=client.mname,
    #         lname=client.lname,
    #         email=client.email,
    #         phone=client.phone,
    #         ssn=client.ssn,
    #         address_line1=client.address_line1,
    #         address_line2=client.address_line2,
    #         zip=client.zip,
    #         city=client.city,
    #         state_abbreviation=client.state.abbreviation,
    #         dob=client.dob,
    #     )
    #     print(res)
    #     #self.assertTrue(res[0])

    # def test_chexsystems(self):
    #     client = self.client
    #     res = Chexsystems().submit(
    #         fname=client.fname,
    #         mname=client.mname,
    #         lname=client.lname,
    #         email=client.email,
    #         phone=client.phone,
    #         ssn=client.ssn,
    #         address_line1=client.address_line1,
    #         address_line2=client.address_line2,
    #         zip=client.zip,
    #         city=client.city,
    #         state_abbreviation=client.state.abbreviation,
    #         dob=client.dob,
    #     )
    #     print(res)
    #     #self.assertTrue(res[0])

    # def test_innovis(self):
    #     client = self.client
    #     res = Innovis().submit(
    #         fname=client.fname,
    #         mname=client.mname,
    #         lname=client.lname,
    #         email=client.email,
    #         phone=client.phone,
    #         ssn=client.ssn,
    #         address_line1=client.address_line1,
    #         address_line2=client.address_line2,
    #         zip=client.zip,
    #         city=client.city,
    #         state_abbreviation=client.state.abbreviation,
    #         dob=client.dob,
    #     )
    #     print(res)
    #     #self.assertTrue(res[0])


    # def test_ars_consumeroffice(self):
    #     client = self.client
    #     res = ARS().submit(
    #         fname=client.fname,
    #         mname=client.mname,
    #         lname=client.lname,
    #         email=client.email,
    #         phone=client.phone,
    #         ssn=client.ssn,
    #         address_line1=client.address_line1,
    #         address_line2=client.address_line2,
    #         zip=client.zip,
    #         city=client.city,
    #         state_abbreviation=client.state.abbreviation,
    #         id_card=client.id_card,
    #         passport=client.passport,
    #         driver_license=client.driver_license
    #     )
    #     print(res)
        #self.assertTrue(res[0])

    # def test_LexisNexis(self):
    #     client = self.client
    #     res = LexisNexis().submit(
    #         fname=client.fname,
    #         mname=client.mname,
    #         lname=client.lname,
    #         email=client.email,
    #         phone=client.phone,
    #         ssn=client.ssn,
    #         address_line1=client.address_line1,
    #         address_line2=client.address_line2,
    #         zip=client.zip,
    #         city=client.city,
    #         state_abbreviation=client.state.abbreviation
    #     )
    #     print(res)
    #     self.assertTrue(res[0])

    # def test_Corelogic(self):
    #     client = self.client
    #     res = Corelogic().submit(fname=client.fname, lname=client.lname, email=client.email)
    #     print(res)
    #     self.assertTrue(res[0])
    #     self.assertIn('Thank you', res[1])