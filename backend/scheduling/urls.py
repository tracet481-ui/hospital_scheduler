from django.urls import path
from .views import GenerateScheduleView, SchedulePlanListView, login_view


urlpatterns = [


    ##  api bağlandı
    path("auth/login/", login_view, name="login"),
    path("schedules/generate/", GenerateScheduleView.as_view()),
    path("schedules/", SchedulePlanListView.as_view()),

]

