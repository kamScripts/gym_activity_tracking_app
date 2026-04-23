from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import MuscleGroup, EquipmentType, Exercise
from .serializers import MuscleGroupSerializer, EquipmentTypeSerializer, ExerciseSerializer

class MuscleGroupViewSet(ReadOnlyModelViewSet):
    queryset = MuscleGroup.objects.all().order_by('name')
    serializer_class = MuscleGroupSerializer

class EquipmentTypeViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentType.objects.all().order_by('name')
    serializer_class = EquipmentTypeSerializer

class ExerciseViewSet(ReadOnlyModelViewSet):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        queryset = Exercise.objects.select_related(
            'muscle_group', 'equipment_type'
        ).order_by('name')

        muscle_group = self.request.query_params.get('muscle_group')
        equipment_type = self.request.query_params.get('equipment_type')
        is_compound = self.request.query_params.get('is_compound')

        if muscle_group:
            queryset = queryset.filter(muscle_group_id=muscle_group)
        if equipment_type:
            queryset = queryset.filter(equipment_type_id=equipment_type)
        if is_compound is not None:
            queryset = queryset.filter(is_compound=is_compound.lower() == 'true')

        return queryset

