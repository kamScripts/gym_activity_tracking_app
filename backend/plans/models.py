from django.db import models
from django.conf import settings
import uuid
from exercises.models import Exercise


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class WorkoutPlan(TimeStamped):
    """Workout Plan consists of N weeks of M workouts per week"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plans'
    )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    goal = models.CharField(max_length=50, blank=True, null=True)
    length_weeks = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class WorkoutUnit(models.Model):
    """Workout Unit - set of X exercises to complete in 1 unit of time"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='units'
    )
    weekly_order = models.IntegerField() #1 - first training in a week 2 - second etc.
    name = models.CharField(max_length=50, blank=True, null=True)
    warmup_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['weekly_order']
        unique_together = [['plan', 'weekly_order']]

    def __str__(self):
        return f"{self.plan.name} - Day {self.weekly_order}"

class PlanExercise(models.Model):
    """PlanExercise model adds plan parameters to the exercise"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(
        WorkoutUnit,
        on_delete=models.CASCADE,
        related_name='plan_exercises'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT,
        related_name='plan_exercises'
    )
    order_index = models.IntegerField()
    default_sets = models.IntegerField()
    rep_range_min = models.IntegerField()
    rep_range_max = models.IntegerField()
    rest_seconds = models.IntegerField()

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return f"{self.exercise.name} in {self.unit}"
