from django.urls import path, include
from rest_framework_nested import routers
from .views import WorkoutViewSet, SetViewSet

router = routers.SimpleRouter()
router.register('workouts', WorkoutViewSet, basename='workout')

workouts_router = routers.NestedSimpleRouter(router, 'workouts', lookup='workout')
workouts_router.register('sets', SetViewSet, basename='workout-sets')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(workouts_router.urls)),
]