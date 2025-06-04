from django.urls import path
from .views import IndexViewTask

urlpatterns = [
    path('', IndexViewTask.as_view()),
]
