from celery import shared_task
from push_notifications.models import GCMDevice


@shared_task
def send_message_helper(user_id: str, title: str, message: str):
    device = GCMDevice.objects.get(user_id=user_id)
    device.send_message(title=title, message=message)