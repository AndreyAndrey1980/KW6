from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    periodicity = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.duration > 120:
            raise ValidationError('Duration cannot exceed 120 seconds.')
        if self.linked_habit and self.reward:
            raise ValidationError('Cannot set both linked habit and reward.')
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError('Linked habit must be a pleasant habit.')
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError('Pleasant habits cannot have rewards or linked habits.')
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError('Periodicity must be between 1 and 7 days.')

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.time} in {self.place}"