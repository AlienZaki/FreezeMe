from celery import shared_task
from time import sleep
from .models import Submission, Website


@shared_task
def submit_async(submission_id):
    submission = Submission.objects.get(id=submission_id)
    print(f'=> Submission {submission_id}: Started! ')
    # Doing submission
    sleep(10)
    # Done submission
    submission.finished = True
    submission.succeed = True
    submission.save()
    print(f'=> Submission {submission_id}: Finished!')
    return


