from django.urls import path

from .views import ( 
                GenerateScheduleView, 
                SchedulePlanListView, 
                # ScheduleListView,
                ScheduleDetailView,
                login_view,
                LatestScheduleView,
                PatientListView,
                SurgeryTypeListView,
                SurgeryRequestListCreateView,
                SimulationPlanDetailView,
                )


urlpatterns = [


    ##  api bağlandı
    path("auth/login/", login_view, name="login"),
    path("schedules/generate/", GenerateScheduleView.as_view()),
    path("schedules/", SchedulePlanListView.as_view(), name= "schedule-plan-list"),
    path("schedules/latest/", LatestScheduleView.as_view(), name = "schedule-latest"),
    path("schedules/<uuid:plan_id>/", ScheduleDetailView.as_view(), name="schedule-detail"),

    ##  operasyon ekleme   ------------------------
    path("surgery-requests/", SurgeryRequestListCreateView.as_view(), name="surgery-request-list-create",),



path(
    "patients/",
    PatientListView.as_view(),
    name="patient-list",
),

path(
    "surgery-types/",
    SurgeryTypeListView.as_view(),
    name="surgery-type-list",
),


path(
    "surgery-requests/",
    SurgeryRequestListCreateView.as_view(),
    name="surgery-request-list-create",
),


path(
    "schedules/<uuid:plan_id>/simulations/<int:valid_index>/",
    SimulationPlanDetailView.as_view(),
    name = "simulation-plan-detail",
),



]



