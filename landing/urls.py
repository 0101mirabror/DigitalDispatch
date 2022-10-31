from django.urls import path
from .views import GetLanding

urlpatterns = [
    path('', GetLanding.as_view(), name='landing')
    ]