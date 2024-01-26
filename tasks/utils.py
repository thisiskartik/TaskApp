import datetime


def get_task_priority(task_due_date):
    days = (task_due_date - datetime.date.today()).days
    priority = 0
    if days == 0:
        priority = 0
    elif 1 <= days <= 2:
        priority = 1
    elif 3 <= days <= 4:
        priority = 2
    elif days >= 5:
        priority = 3
    return priority
