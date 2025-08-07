from django.urls import path
from .views import *

urlpatterns = [
    path('' , ListCreateApiView.as_view()),
]