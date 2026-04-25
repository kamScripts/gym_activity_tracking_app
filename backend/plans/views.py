from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import WorkoutPlan, WorkoutUnit, PlanExercise
from .serializers import (
    WorkoutPlanSerializer, WorkoutUnitSerializer, PlanExerciseSerializer
)


class WorkoutPlanViewSet(ModelViewSet):
    serializer_class = WorkoutPlanSerializer

    def get_queryset(self):
        return WorkoutPlan.objects.filter(
            user=self.request.user
        ).prefetch_related('units__plan_exercises__exercise')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutUnitViewSet(ModelViewSet):
    serializer_class = WorkoutUnitSerializer

    def get_queryset(self):
        plan_id = self.kwargs['plan_id']
        return WorkoutUnit.objects.filter(
            plan_id=plan_id,
            plan__user=self.request.user
        )

    def perform_create(self, serializer):
        plan_id = self.kwargs['plan_id']
        try:
            plan = WorkoutPlan.objects.get(id=plan_id, user=self.request.user)
        except WorkoutPlan.DoesNotExist:
            raise NotFound('Plan not found')
        serializer.save(plan=plan)


class PlanExerciseViewSet(ModelViewSet):
    serializer_class = PlanExerciseSerializer

    def get_queryset(self):
        unit_id = self.kwargs['unit_id']
        return PlanExercise.objects.filter(
            unit_id=unit_id,
            unit__plan__user=self.request.user
        )

    def perform_create(self, serializer):
        unit_id = self.kwargs['unit_id']
        try:
            unit = WorkoutUnit.objects.get(
                id=unit_id,
                plan__user=self.request.user
            )
        except WorkoutUnit.DoesNotExist:
            raise NotFound('Unit not found')
        serializer.save(unit=unit)
