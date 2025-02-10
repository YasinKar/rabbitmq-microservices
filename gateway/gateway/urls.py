from django.urls import re_path
from .views import APIGatewayView

urlpatterns = [
    re_path(r'^(?P<path>.*)$', APIGatewayView.as_view()),
]