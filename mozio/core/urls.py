from django.urls import path

from .views import UserListView, ServiceAreaListView, ServiceDetailView, UserDetailView

app_name = "mozio.core"

urlpatterns = [
    path('v1/users/', UserListView.as_view(), name="user-list"),
    path('v1/users/<int:pk>/', UserDetailView.as_view(), name="user-details"),
    path('v1/service-area/', ServiceAreaListView.as_view(), name="service-list"),
    path('v1/service-area/<int:pk>/', ServiceDetailView.as_view(), name="service-details"),
]
