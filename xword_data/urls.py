from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name='login'),
    path("drill", views.DrillView.as_view(), name='drill'),
    path("answer", views.AnswerView.as_view(), name='answer'),

]