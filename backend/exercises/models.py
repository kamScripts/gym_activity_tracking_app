from django.db import models
import uuid

class MuscleGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class EquipmentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.PROTECT,
        related_name='exercises'
    )
    equipment_type = models.ForeignKey(    # ← snake_case field name
        EquipmentType,                     #    PascalCase class reference
        on_delete=models.PROTECT,
        related_name='exercises',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    is_compound = models.BooleanField(default=False)

    def __str__(self):
        return self.name
