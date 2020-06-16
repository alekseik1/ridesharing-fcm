from celery import shared_task
from push_notifications.models import GCMDevice
from django.contrib.auth.models import User
from django.http import HttpResponse


@shared_task
def update_token(user_id: str, new_token: str):
    try:
        device = GCMDevice.objects.get(user_id=user_id)
        device.registration_id = new_token
    except GCMDevice.DoesNotExist:
        user = User(pk=user_id, username=user_id)
        user.save()
        device = GCMDevice(user_id=user_id, registration_id=new_token, cloud_message_type='FCM')
    device.save()


@shared_task
def send_message_helper(user_id: str, title: str, message: str):
    device = GCMDevice.objects.get(user_id=user_id)
    device.send_message(title=title, message=message)