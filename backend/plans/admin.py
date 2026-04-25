from django.contrib import admin

from exercises.models import MuscleGroup, Exercise
from plans.models import WorkoutPlan, WorkoutUnit, PlanExercise


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'user', 'id')

@admin.register(WorkoutUnit)
class WorkoutUnitAdmin(admin.ModelAdmin):
    list_display = ('weekly_order', 'plan')
    ordering = ('weekly_order','plan')

@admin.register(PlanExercise)
class PlanExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise','order_index', 'default_sets',
            'rep_range_min', 'rep_range_max', 'rest_seconds',
            'id',
                    )
