from django.db import models
from users.models import User


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    priority = models.PositiveSmallIntegerField(choices=(
        (0, "0"),
        (1, "1-2"),
        (2, "3-4"),
        (3, "5+")
    ))
    status = models.CharField(max_length=200, choices=(
        ("TODO", "Todo"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done")
    ), default="DONE")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} | {self.due_date} - {self.priority}"
