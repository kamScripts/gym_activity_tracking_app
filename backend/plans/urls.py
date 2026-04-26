from django.urls import path, include
from rest_framework_nested import routers

from workouts.views import PrefillView
from .views import WorkoutPlanViewSet, WorkoutUnitViewSet, PlanExerciseViewSet

router = routers.SimpleRouter()
router.register('plans', WorkoutPlanViewSet, basename='plan')

plans_router = routers.NestedSimpleRouter(router, 'plans', lookup='plan')
plans_router.register('units', WorkoutUnitViewSet, basename='plan-units')

units_router = routers.NestedSimpleRouter(plans_router, 'units', lookup='unit')
units_router.register('exercises', PlanExerciseViewSet, basename='unit-exercises')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(plans_router.urls)),
    path('', include(units_router.urls)),
    path(
        'plans/<uuid:plan_id>/units/<uuid:unit_id>/prefill/',
        PrefillView.as_view(),
        name='prefill'
    ),
]