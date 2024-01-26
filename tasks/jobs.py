from time import sleep
from urllib.parse import urlencode
from datetime import date
from .models import Task
from .utils import get_task_priority
from taskapp.twilio import call


def update_task_priority():
    print("Updating task priority")
    for task in Task.objects.filter(is_deleted=False):
        task.priority = get_task_priority(task.due_date)
        task.save()


def notify_expired_tasks():
    for task in Task.objects.filter(is_deleted=False, due_date__lt=date.today()).exclude(status='DONE').order_by('user__priority'):
        print(f"CALLING {task.user.phone_number} [priority: {task.user.priority}] for task {task.title} with priority")
        call(to=f"{task.user.country_code}{task.user.phone_number}",
             url=f"https://eb9k4g2bcd.execute-api.ap-south-1.amazonaws.com/default/OpenInApp?{urlencode({'task_title': task.title})}")
        sleep(5)
