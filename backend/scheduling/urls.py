from django.urls import path
from .views import ( 
                GenerateScheduleView, 
                SchedulePlanListView, 
                # ScheduleListView,
                ScheduleDetailView,
                login_view,
                LatestScheduleView,
                )


urlpatterns = [


    ##  api bağlandı
    path("auth/login/", login_view, name="login"),
    path("schedules/generate/", GenerateScheduleView.as_view()),
    path("schedules/", SchedulePlanListView.as_view(), name= "schedule-plan-list"),
    path("schedules/latest/", LatestScheduleView.as_view(), name = "schedule-latest"),
    path("schedules/<uuid:plan_id>/", ScheduleDetailView.as_view(), name="schedule-detail"),

]

