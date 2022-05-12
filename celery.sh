#!/bin/sh

celery -A FreezeMe worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l info
celery -A FreezeMe flower --address=0.0.0.0 --port5566