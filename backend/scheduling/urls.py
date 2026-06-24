from django.urls import path
from .views import GenerateScheduleView, SchedulePlanListView


urlpatterns = [


    ##  api bağlandı
    path ("generate/", GenerateScheduleView.as_view(), name = "generate-schedule"),
    path ("", SchedulePlanListView.as_view(), name = "schedule-plan-list"),

]

