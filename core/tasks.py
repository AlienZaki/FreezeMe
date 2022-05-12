from celery import shared_task
from time import sleep
from .models import Submission, Website


@shared_task
def submit_async():
    #sleep(10)
    client_id = 1
    Submission.objects.create(
        client_id=client_id,
        website=Website.objects.first(),
        finished=True,
        succeed=True,
    )
    print('=> Submitted', client_id)
    return


