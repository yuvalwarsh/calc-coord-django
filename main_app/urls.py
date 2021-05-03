from django.urls import path
from . import views as main_app_views

urlpatterns = [
    path('', main_app_views.home, name='homepage'),
    path('pts/<newdoc_uuid>/', main_app_views.pts, name='pts'),
    path('links/<newdoc_uuid>/', main_app_views.links, name='links'),
    path('users/<str:username>/points-list/', main_app_views.UserPointsListView.as_view(), name='user-points'),
    path("/users/<str:username>/delete/<uuid>/", main_app_views.CustomDeleteView.as_view(), name="delete-doc")
]
