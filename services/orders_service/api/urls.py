from django.urls import path
from .views import PlaceOrderView

urlpatterns = [
    path('place-order/', PlaceOrderView.as_view(), name='place_order')
]