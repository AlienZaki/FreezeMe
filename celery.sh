#!/bin/sh

celery -A FreezeMe worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l info