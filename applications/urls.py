"""Router configuration for the applications API."""

from rest_framework.routers import DefaultRouter

from .views import JobApplicationViewSet

router = DefaultRouter()
# Registering a ViewSet with the router automatically creates the CRUD routes.
router.register('applications', JobApplicationViewSet, basename='application')

urlpatterns = router.urls
