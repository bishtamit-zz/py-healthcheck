from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("status/<str:name>/", views.CheckStatusView.as_view(), name='status')
]
