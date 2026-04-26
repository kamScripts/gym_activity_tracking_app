from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from plans.models import WorkoutPlan, WorkoutUnit, PlanExercise
from plans.serializers import PlanExerciseSerializer
from .models import Workout, Set
from .serializers import WorkoutSerializer, SetSerializer


class WorkoutViewSet(ModelViewSet):
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        return Workout.objects.filter(
            user=self.request.user
        ).select_related('plan', 'workout_unit').prefetch_related('sets__exercise')

    def perform_create(self, serializer):
        # Validate the plan and unit belong to the user before saving
        plan_id = serializer.validated_data['plan'].id
        unit = serializer.validated_data['workout_unit']

        if not WorkoutPlan.objects.filter(id=plan_id, user=self.request.user).exists():
            raise NotFound('Plan not found')

        if unit.plan_id != plan_id:
            raise NotFound('Unit does not belong to this plan')

        serializer.save(user=self.request.user)


class SetViewSet(ModelViewSet):
    """
    Basic Block of workout
    """
    serializer_class = SetSerializer

    def get_queryset(self):
        workout_id = self.kwargs['workout_pk']
        return Set.objects.filter(
            workout_id=workout_id,
            workout__user=self.request.user
        ).select_related('exercise')

    def perform_create(self, serializer):
        workout_id = self.kwargs['workout_pk']
        try:
            workout = Workout.objects.get(
                id=workout_id, user=self.request.user
            )
        except Workout.DoesNotExist:
            raise NotFound('Workout not found')
        serializer.save(workout=workout)


class PrefillView(APIView):
    """
    Returns plan_exercises for a given unit for workout assistance autocomplete,
    pre-populate the workout form with default sets, reps, rest.
    """
    def get(self, request, plan_id, unit_id):
        # Verify the plan belongs to this user
        try:
            unit = WorkoutUnit.objects.get(
                id=unit_id,
                plan_id=plan_id,
                plan__user=request.user
            )
        except WorkoutUnit.DoesNotExist:
            raise NotFound('Unit not found')

        plan_exercises = PlanExercise.objects.filter(
            unit=unit
        ).select_related('exercise').order_by('order_index')

        serializer = PlanExerciseSerializer(plan_exercises, many=True)
        return Response(serializer.data)
