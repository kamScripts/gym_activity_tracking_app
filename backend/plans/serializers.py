from rest_framework import serializers
from .models import WorkoutPlan, WorkoutUnit, PlanExercise

class PlanExerciseSerializer(serializers.ModelSerializer):

    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = PlanExercise
        fields = [
            'id', 'exercise', 'exercise_name',
            'order_index', 'default_sets',
            'rep_range_min', 'rep_range_max', 'rest_seconds'
        ]

class WorkoutUnitSerializer(serializers.ModelSerializer):

    plan_exercises = PlanExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutUnit
        fields = [
            'id', 'weekly_order', 'name', 'warmup_notes', 'plan_exercises'
        ]

class WorkoutPlanSerializer(serializers.ModelSerializer):

    units = WorkoutUnitSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'description', 'goal', 'length_weeks',
            'is_active', 'created_at', 'updated_at', 'units'
        ]
        read_only_fields = ['created_at', 'updated_at']
