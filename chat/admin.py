from django.contrib import admin
from chat.models import Message,Room

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','body','send_by','created_at','created_by']
    list_display_links=['id','body','send_by']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['id','client','agent','status']
    list_display_links=['id','client','agent']