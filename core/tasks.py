from celery import shared_task
from time import sleep
from .models import Submission, Website
from datetime import datetime
import random
from .automation.corelogic import Corelogic


@shared_task
def submit_async(submission_id):
    submission = Submission.objects.get(id=submission_id)
    print(f'=> Submission {submission_id}: Started! ')
    # Doing submission
    if 'corelogic.com'.lower() in submission.website.url.lower() and submission.website.ready:
        try:
            success, msg = Corelogic().submit(fname=submission.client.fname, lname=submission.client.lname, email=submission.client.email)
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


