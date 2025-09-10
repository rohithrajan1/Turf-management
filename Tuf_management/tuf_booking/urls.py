from django.urls import path,include
from .views import *

urlpatterns = [
    path('signup/',UserSignUpView.as_view(),name = 'user-signup'),
    path('login/',UserLoginView.as_view(),name = 'user-login'),
    path('booking/',BookingView.as_view(),name = 'Turf-booking'),
    path('admin-action/<str:name>/',AdminTurfActionView.as_view(),name = 'admin-turf-action-update'),
    path('admin-action/',AdminTurfActionView.as_view(),name = 'admin-turf-action')
]