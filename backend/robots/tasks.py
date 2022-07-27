from celery import shared_task


@shared_task
def process_location():
    pass


@shared_task
def process_telemetry():
    pass
