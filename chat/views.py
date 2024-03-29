from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from chat.models import Room
from django.contrib.auth.decorators import login_required
from chat.models import User
from account.forms import AddUserForm,EditUserForm
from django.contrib import messages
from django.contrib.auth.models import Group

# Create your views here.

@require_POST
def create_room(request,uuid):
    name = request.POST.get('name','')
    url = request.POST.get('url','')

    Room.objects.create(uuid=uuid,client=name,url=url)

    return JsonResponse({'message':'room created'})

@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)

    return render(request, 'chat/admin.html', {'rooms': rooms, 'users':users})

@login_required
def room(request,uuid):
    room = Room.objects.get(uuid=uuid)

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()

    return render(request, 'chat/room.html', {'room': room})

@login_required
def user_detail(request,uuid):
    user = User.objects.get(pk=uuid)
    rooms = user.rooms.all() # type: ignore

    return render(request, 'chat/user_detail.html',{'user':user,'rooms':rooms})


@login_required
def add_user(request):
    if request.user.has_perm('user.add_user'):
        if request.method == 'POST':
            form = AddUserForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.set_password(request.POST.get('password'))
                user.save()

                if user.role == User.AGENT:
                    group = Group.objects.get(name="Agents")
                    group.user_set.add(user) # type: ignore

                if user.role == User.MANAGER:
                    group = Group.objects.get(name="Managers")
                    group.user_set.add(user) # type: ignore
                
                messages.error(request, "The user was added!")
                return redirect('chat:chat-admin')
        else:
            form = AddUserForm()
        
        return render(request, 'chat/add_user.html', {'form': form})
    else:
        messages.error(request, "You don\'t have access to add users!")
        return redirect('chat:chat-admin')



