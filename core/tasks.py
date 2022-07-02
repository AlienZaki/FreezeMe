from celery import shared_task
from time import sleep
from .models import Submission, Website
from datetime import datetime
import random
from .automation.corelogic import Corelogic
from .automation.lexisNexis import LexisNexis
from .automation.innovis import Innovis
from .automation.chexsystems import Chexsystems
from .automation.telecomUtilityExchange import TelecomUtilityExchange
from .automation.factorTrust import FactorTrust
from .automation.clarityServices import ClarityServices
from .automation.sageStreamOpt import SageStreamOpt
from .automation.sageStream import SageStream


@shared_task
def submit_async(submission_id):
    submission = Submission.objects.get(id=submission_id)
    print(f'=> Submission {submission_id}: Started! ')
    print(f'=> Submission: {submission.client.fname} {submission.client.lname} - {submission.website.name}')
    # Doing submission
    if 'corelogic.com'.lower() in submission.website.url.lower():
        try:
            success, msg = Corelogic().submit(fname=submission.client.fname, lname=submission.client.lname, email=submission.client.email)
        except Exception as e:
            success, msg = False, e
    elif 'optout.lexisnexis.com'.lower() in submission.website.url.lower():
        try:
            success, msg = LexisNexis().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'innovis.com'.lower() in submission.website.url.lower():
        try:
            success, msg = Innovis().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'chexsystems.com'.lower() in submission.website.url.lower():
        try:
            success, msg = Chexsystems().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'exchangeservicecenter.com'.lower() in submission.website.url.lower():
        try:
            success, msg = TelecomUtilityExchange().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'lendprotect.transunion.com'.lower() in submission.website.url.lower():
        try:
            success, msg = FactorTrust().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'consumers.clarityservices.com'.lower() in submission.website.url.lower():
        try:
            success, msg = ClarityServices().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'forms.sagestreamllc.com'.lower() in submission.website.url.lower():
        try:
            success, msg = SageStreamOpt().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    elif 'forms.consumer.risk.lexisnexis.com'.lower() in submission.website.url.lower():
        try:
            success, msg = SageStream().submit(
                fname=submission.client.fname,
                mname=submission.client.mname,
                lname=submission.client.lname,
                email=submission.client.email,
                phone=submission.client.phone,
                dob=submission.client.dob,
                ssn=submission.client.ssn,
                address_line1=submission.client.address_line1,
                address_line2=submission.client.address_line2,
                zip=submission.client.zip,
                city=submission.client.city,
                state_abbreviation=submission.client.state.abbreviation
            )
        except Exception as e:
            success, msg = False, e
    else:
        success, msg = False, 'Couldn\'t find the automation script.'

    # Save result
    submission.finish_time = datetime.now()
    submission.finished = True
    submission.succeed = success
    submission.note = msg
    submission.save()
    print(f'=> Submission {submission_id}: Finished!')
    return


