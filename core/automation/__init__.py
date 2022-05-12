from .captcha import CaptchaSolver
from ..models import Client, Website, Submission, Settings, State
from ..tasks import submit_async
from datetime import datetime


def task_manager(client):
    # select only the ready websites
    websites = Website.objects.filter(ready=True).all()
    for website in websites:
        # record the tasks as pending
        submission, created = Submission.objects.get_or_create(
            client=client,
            website=website,
        )
        if not created:
            # reset values
            submission.finished = False
            submission.succeed = False
            submission.timestamp = datetime.now()
            submission.finish_time = None
            submission.save()

        # send to worker
        submit_async.delay(submission_id=submission.id)



def resubmit_task(submission):
    # reset values
    submission.finished = False
    submission.succeed = False
    submission.timestamp = datetime.now()
    submission.finish_time = None
    submission.save()

    # send to worker
    submit_async.delay(submission_id=submission.id)