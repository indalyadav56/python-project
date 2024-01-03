from django.urls import path

from main.views import UserAPIView

urlpatterns = [
    path('', UserAPIView.as_view(), name='user'),
]
