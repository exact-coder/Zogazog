from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User

# Create your models here.

class Message(models.Model):
    body = models.TextField(_("Message"))
    send_by = models.CharField(_("Send By"), max_length=255)
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User,blank=True,null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f'{self.send_by}'
    
class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    )

    uuid = models.CharField(_("UUID"), max_length=255)
    client = models.CharField(_("Client"), max_length=255)
    agent = models.ForeignKey(User, related_name='rooms',blank=True,null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(_("URL"), max_length=255,blank=True,null=True)
    status = models.CharField(_("STATUS"), max_length=20,choices=CHOICES_STATUS,default=WAITING)
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.client} - {self.uuid}'