# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', FlowerListCreateAPIView.as_view()),
    path('u/<int:pk>/', FlowerDetailAPIView.as_view()),
]
