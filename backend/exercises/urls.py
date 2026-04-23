from rest_framework.routers import DefaultRouter
from .views import MuscleGroupViewSet, EquipmentTypeViewSet, ExerciseViewSet

router = DefaultRouter()
router.register('muscle-groups', MuscleGroupViewSet, basename='muscle-group')
router.register('equipment-types', EquipmentTypeViewSet, basename='equipment-type')
router.register('exercises', ExerciseViewSet, basename='exercise')

urlpatterns = router.urls