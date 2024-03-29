from django.urls import path
from chat import views

app_name= 'chat'

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name="create-room"),
    path('chat-admin/', views.admin, name="chat-admin"),
    path('chat-admin/add_user/', views.add_user, name="add_user"),
    path('chat-admin/<uuid:uuid>/edit/', views.edit_user, name="edit_user"),
    path('chat-admin/users/<uuid:uuid>/', views.user_detail, name="user_detail"),
    path('chat-room/<str:uuid>/', views.room, name="chat-room"),
]
