from django.urls import path
from .views import (
    RoomMembersView,
    RoomView, 
    TaskView,
    TaskGroupsView,
    OneRoomView
)

urlpatterns = [
    path('members/', RoomMembersView.as_view()),
    path('room/', RoomView.as_view()),
    path('room/<str:room_name>', OneRoomView.as_view()),
    path('task/', TaskView.as_view()),
    path('task-groups/', TaskGroupsView.as_view()),
]