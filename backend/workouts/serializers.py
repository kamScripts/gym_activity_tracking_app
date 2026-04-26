from rest_framework import serializers
from .models import Workout, Set


class SetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = Set
        fields = [
            'id', 'exercise', 'exercise_name',
            'set_number', 'reps', 'weight_kg',
            'rest_after_seconds', 'logged_at'
        ]
        read_only_fields = ['logged_at']


class WorkoutSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    unit_name = serializers.CharField(source='workout_unit.name', read_only=True)

    class Meta:
        model = Workout
        fields = [
            'id', 'plan', 'plan_name',
            'workout_unit', 'unit_name',
            'started_at', 'completed_at',
            'warmup_notes', 'notes', 'sets'
        ]
        read_only_fields = ['started_at']