from django.db import models
from django.conf import settings
import uuid
from plans.models import WorkoutPlan, WorkoutUnit
from exercises.models import Exercise

class Workout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.PROTECT,
        related_name='workouts'
    )
    workout_unit = models.ForeignKey(
        WorkoutUnit,
        on_delete=models.PROTECT,
        related_name='workouts'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    warmup_notes = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at'] # ORDER BY started_at DESC

    def __str__(self):
        return f"{self.user.username} - {self.started_at:%Y-%m-%d}"


class Set(models.Model):
    """exercise set"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='sets'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT,
        related_name='sets'
    )
    set_number = models.IntegerField()
    reps = models.IntegerField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rest_after_seconds = models.IntegerField(blank=True, null=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['logged_at']

    def __str__(self):
        return f"{self.exercise.name} set {self.set_number}"
