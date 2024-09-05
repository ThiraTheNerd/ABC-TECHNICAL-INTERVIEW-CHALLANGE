from django.urls import path
from .views import OwnerStatsView, VehicleStatsView, FileUploadView, FileListView, FileSummaryView
from . import views
urlpatterns = [
    path('services/', views.get_services, name='service_list'),
    path('owners/stats/', OwnerStatsView.as_view(), name='owner_statistics'),
    path('vehicles/stats/', VehicleStatsView.as_view(), name='vehicle_statistics'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('summary/', FileSummaryView.as_view(), name='file-summary'),
]
