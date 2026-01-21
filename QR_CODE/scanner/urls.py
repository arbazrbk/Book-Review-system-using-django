from django.urls import path
from scanner.views import generate,scan

urlpatterns = [
    path('generate/',generate,name="generate"),
    path('sca/',scan,name="scanner"),
]