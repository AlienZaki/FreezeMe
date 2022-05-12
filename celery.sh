#!/bin/sh

celery -A FreezeMe worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l info
celery -A FreezeMe flower --address=127.0.0.6 --port5566