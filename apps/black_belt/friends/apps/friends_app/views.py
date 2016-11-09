from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
from .models import Friendship, User

# Create your views here.

def index(request):
    return render(request, 'friends_app/index.html')

def register(request):
    if request.method == 'POST':
        errors, user = User.objects.register(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, "Welcome {}!".format(user.alias))
            request.session['current_id'] = user.id
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors, user = User.objects.login(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, "Welcome {}!".format(user.alias))
            request.session['current_user'] = user.id
    return redirect ('/friends')

def friends(request):
    if not 'current_user' in request.session:
        return redirect ('/')
    current_user = User.objects.get(id=request.session['current_user'])
    users = User.objects.all().exclude(id=request.session['current_user'])
    friends = Friendship.objects.filter(user=current_user)  

    context = {'current_user': current_user, 'users': users, 'friends': friends}
    return render(request, 'friends_app/friends.html', context)

def add_friend(request, id):
    if not 'current_user' in request.session:
        return redirect ('/')
    user = User.objects.get(id=request.session['current_user'])
    friend = User.objects.get(id=id)
    Friendship.objects.create(user=user, friend=friend)
    return redirect ('/friends')

def remove_friend(request, id):
    if not 'current_user' in request.session:
        return redirect ('/')
    user = User.objects.get(id=request.session['current_user'])
    friend = User.objects.get(id=id)
    Friendship.objects.filter(user=user, friend=friend).delete()
    Friendship.objects.filter(user=friend, friend=user).delete()
    return redirect ('/friends')

def user(request, id):
    if not 'current_user' in request.session:
        return redirect ('/')
    user = User.objects.get(id=id)
    context = {'user': user}
    return render (request, 'friends_app/user.html', context)

def logout(request):
    if not 'current_user' in request.session:
        return redirect ('/')
    request.session.pop('current_user')
    return redirect ('/')