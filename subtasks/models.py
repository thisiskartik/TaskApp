from django.db import models
from tasks.models import Task


class SubTask(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=(
        (0, "Incomplete"),
        (1, "Complete")
    ))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} | {self.status}"
