from rest_framework import serializers
from .models import MuscleGroup, EquipmentType, Exercise

class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name']

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ['id', 'name']

class ExerciseSerializer(serializers.ModelSerializer):
    muscle_group_name = serializers.CharField(source='muscle_group', read_only=True)
    equipment_type_name = serializers.CharField(source='equipment_type', read_only=True, default=None)
    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'is_compound', 'muscle_group', 'muscle_group_name',
            'equipment_type', 'equipment_type_name'
        ]