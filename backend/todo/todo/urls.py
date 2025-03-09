from django.contrib import admin
from django.urls import path
from . import views  # ✅ This is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.signup)  # Ensure `signup` exists in views.py
]
