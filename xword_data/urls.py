from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("drill/", views.DrillView.as_view(), name='xword-drill'),
    path("answer/", views.AnswerView.as_view(), name='xword-answer'),

]