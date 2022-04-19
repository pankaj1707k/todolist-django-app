from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    task = models.TextField(_("task"))
    due_date = models.DateField(_("due date"), blank=True, null=True)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    completed = models.BooleanField(_("completed"), default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"#{self.id}: {self.task if len(self.task)<20 else (self.task[:20]+'...')}"
        )
