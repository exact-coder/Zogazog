from django.urls import path
from chat import views

app_name= 'chat'

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name="create-room"),
]
