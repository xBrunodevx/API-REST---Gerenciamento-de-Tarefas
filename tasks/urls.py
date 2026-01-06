from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, TaskViewSet

auth_urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

task_urlpatterns = router.urls
