from django.contrib import admin

from .models import Workout, Set


@admin.register(Workout)
class Workout(admin.ModelAdmin):
    list_display = ('user', 'id', 'started_at', 'completed_at', 'plan', 'plan_id', 'workout_unit', 'workout_unit_id')

@admin.register(Set)
class Set(admin.ModelAdmin):
    list_display = ('id', 'workout', 'workout_id', 'set_number', 'logged_at', 'exercise')
