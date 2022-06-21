from celery import shared_task
from time import sleep
from .models import Submission, Website
from datetime import datetime
import random
from .automation.corelogic import Corelogic
from .automation.lexisNexis import LexisNexis
from .automation.innovis import Innovis


@shared_task
def submit_async(submission_id):
    submission = Submission.objects.get(id=submission_id)
    print(f'=> Submission {submission_id}: Started! ')
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


