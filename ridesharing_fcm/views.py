from push_notifications.models import GCMDevice
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse


def update_firebase_token(request):
    """
    Update Firebase ID for device with device_id

    :param request: POST {'id', 'token'}, 'token' is new token
    """
    new_token, user_id = request.POST['token'], request.POST['id']
    try:
        device = GCMDevice.objects.get(user_id=user_id)
        device.registration_id = new_token
    except GCMDevice.DoesNotExist:
        user = User(pk=user_id, username=user_id)
        user.save()
        device = GCMDevice(user_id=user_id, registration_id=new_token, cloud_message_type='FCM')
    device.save()
    return HttpResponse('ok')


def send_message_immediately(request):
    """
    Send message to one user immediately

    :param request: GET {'id', 'title', 'body'}
    """
    user_id = request.GET['id']
    title, message = request.GET['title'], request.GET['message']
    device = get_object_or_404(GCMDevice, user_id=user_id)
    device.send_message(title=title, message=message)
    return HttpResponse('ok')
