from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/create/", views.create_room, name="create_room"),
    path("room/<int:room_id>/", views.room_detail, name="room_detail"),
    path("room/<int:room_id>/join/", views.join_room, name="join_room"),
    path("room/<int:room_id>/leave/", views.leave_room, name="leave_room"),
]
