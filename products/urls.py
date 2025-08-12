from django.urls import path
from .views import *

urlpatterns = [
    path('', RegisterApi.as_view()),
    path('login/', LoginApi.as_view()),
    path('logout/', LogoutView.as_view()),
    path('u', FlowerListCreateView.as_view()),
    path('u/<int:pk>/', FlowerDetailView.as_view()),
    path('profile/' , ProfileApi.as_view())
]

