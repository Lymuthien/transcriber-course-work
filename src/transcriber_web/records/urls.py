from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.AudioUploadView.as_view(), name="upload"),
    path("", views.RecordListView.as_view(), name="record_list"),
    path("<str:record_id>/", views.RecordDetailView.as_view(), name="record_detail"),
]
