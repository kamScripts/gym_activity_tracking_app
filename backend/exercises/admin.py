from django.contrib import admin

from exercises.models import MuscleGroup, EquipmentType, Exercise


@admin.register(MuscleGroup)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ("name", "id")

@admin.register(EquipmentType)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ("name", "id")

@admin.register(Exercise)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ("name","equipment_type","muscle_group","is_compound", "id")
