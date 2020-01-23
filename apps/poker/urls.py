from django.urls import path

from .views import (
    CreateRoomView,
    IndexView,
    MemberView,
    RoomHistoryView,
    RoomView,
    SettingsView,
    StatusView,
)

app_name = 'apps.poker'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateRoomView.as_view(), name='create'),
    path('rooms/<token>/', RoomView.as_view(), name='room'),
    path('rooms/<token>/history/', RoomHistoryView.as_view(), name='history'),
    path('rooms/<token>/member/', MemberView.as_view(), name='member'),
    path('rooms/<token>/status/', StatusView.as_view(), name='status'),
    path('rooms/<token>/settings/', SettingsView.as_view(), name='settings'),
]
