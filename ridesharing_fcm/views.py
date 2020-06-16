from datetime import datetime

from django.http import HttpResponse

from ridesharing_fcm.tasks import send_message_helper, update_token


def update_firebase_token(request):
    """
    Update Firebase ID for device with device_id

    :param request: POST {'id', 'token'}, 'token' is new token
    """
    new_token, user_id = request.POST['token'], request.POST['id']
    update_token(user_id, new_token)
    return HttpResponse('ok')


def send_message_immediately(request):
    """
    Send message to one user immediately

    :param request: GET {'id', 'title', 'body'}
    """
    user_id = request.GET['id']
    title, message = request.GET['title'], request.GET['message']
    send_message_helper.delay(user_id=user_id, title=title, message=message)
    return HttpResponse('ok')


def send_message_datetime(request):
    """
    Send message at given time. Time is timestamp
    :param request: GET {'id', 'title', 'body', 'timestamp'}
    """
    user_id, timestamp = request.GET['id'], request.GET['timestamp']
    time = datetime.fromtimestamp(int(float(timestamp)))
    title, message = request.GET['title'], request.GET['message']
    send_message_helper.apply_async((user_id, title, message), eta=time)
    return HttpResponse('ok')
