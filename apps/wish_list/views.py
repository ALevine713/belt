from django.shortcuts import render, HttpResponse, redirect
from .models import User, Wish
from django.contrib import messages
import datetime
# Create your views here.

def index(request):
    return render(request, 'wish_list/index.html')

def register(request):
    if request.method == 'POST':
        data = {
            'name': request.POST['name'],
            'username': request.POST['username'],
            'e_address': request.POST['email'],
            'pass_word': request.POST['password'],
            'confirm_pass_word': request.POST['pw_confirm'],
        }
        new_user = User.objects.reg(data)
        if new_user['error_list']: #connected to lines 39 and 45 in models.py
            for error in new_user['error_list']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        else:
            request.session['user_id'] = new_user['new'].id
            request.session['user_name'] = new_user['new'].username
            return redirect('/dashboard')

def login(request):
    if request.method == 'POST':
        data = {
            'e_mail': request.POST['email'],
            'p_word': request.POST['password'],
        }
        a_user = User.objects.log(data)
        if a_user['list_errors']: #connected to lines 39 and 45 in models.py
            for error in a_user['list_errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        else:
            request.session['user_id'] = a_user['logged_user'].id
            request.session['user_name'] = a_user['logged_user'].username
            return redirect('/dashboard')

def dashboard(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_added_wishs': Wish.objects.filter(users = current_user),
        'user_created_wishs': Wish.objects.filter(creator = current_user),
        'other_wishes': Wish.objects.exclude(users = current_user).exclude(creator = current_user)
    }
    return render(request, 'wish_list/dashboard.html', context)

def new_wish(request):
    return render(request, 'wish_list/new_wish.html')

def add_wish(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'], username=request.session['user_name'])
        data = {
            'item': request.POST['item'],
            'creator': current_user,
        }
        new_wish = Wish.objects.new(data)
        if new_wish['error_list']: #connected to lines 39 and 45 in models.py
            for error in new_wish['error_list']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/new_wish')
        else:
            return redirect('/dashboard')
    return redirect ('/dashboard')

def include_wish(request, wish_id):
    current_user = User.objects.get(id=request.session['user_id'])
    wish = Wish.objects.get(id = wish_id)
    wish.users.add(current_user)
    return redirect('/dashboard')

def wish_info(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    context = {
        "wish": wish,
    }
    return render(request, 'wish_list/wish_item.html', context)

def remove_wish(request, wish_id):
    current_user = User.objects.get(id=request.session['user_id'])
    wish = Wish.objects.get(id=wish_id)
    wish.users.remove(current_user)
    return redirect ('/dashboard')

def delete(request, wish_id):
    Wish.objects.get(id = wish_id).delete()
    return redirect ('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
