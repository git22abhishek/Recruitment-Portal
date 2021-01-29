from django.urls import path
from .views import JobList

urlpatterns = [
    path('', JobList, name='joblist'),
]
