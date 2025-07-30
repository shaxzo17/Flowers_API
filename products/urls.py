# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # with mixins
    # path('', FlowerListCreateView.as_view()),
    # path('u/<int:pk>/', FlowerDel.as_view()),

    # without mixins
    path('', FlowerListCreateAPIView.as_view()),
    path('u/<int:pk>/', FlowerDetailAPIView.as_view()),
]
