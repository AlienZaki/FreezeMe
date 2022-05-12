from celery import shared_task
from time import sleep
from .models import Submission, Website
from datetime import datetime
import random


@shared_task
def submit_async(submission_id):
    submission = Submission.objects.get(id=submission_id)
    print(f'=> Submission {submission_id}: Started! ')
    # Doing submission
    sleep(30)
    # Done submission

    # Save result
    submission.finish_time = datetime.now()
    submission.finished = True
    submission.succeed = random.choice([True, False])   # random just for test
    submission.save()
    print(f'=> Submission {submission_id}: Finished!')
    return


