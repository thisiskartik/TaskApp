from django.db import models
from django.dispatch import receiver
from .models import SubTask


@receiver(models.signals.post_save, sender=SubTask)
def update_task_on_save(sender, instance, **kwargs):
    complete = 0
    incomplete = 0
    for subtask in instance.task.subtask_set.filter(is_deleted=False):
        if subtask.status == 0:
            incomplete += 1
        elif subtask.status == 1:
            complete += 1

    if incomplete == 0:
        instance.task.status = "DONE"
    elif complete == 0:
        instance.task.status = "TODO"
    elif complete >= 1:
        instance.task.status = "IN_PROGRESS"
    instance.task.save()
