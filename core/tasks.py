from celery import shared_task
from time import sleep
from .models import Submission, Website


@shared_task
def submit_async():
    #sleep(10)
    celint_id = 1
    Submission.objects.create(
        celint_id=celint_id,
        website=Website.objects.first(),
        finished=True,
        succeed=True,
    )
    print('=> Submitted', celint_id)
    return


