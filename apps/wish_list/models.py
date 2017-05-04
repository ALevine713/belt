from __future__ import unicode_literals

from django.db import models
import re, datetime, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg(self, data):
        errors = []
        if len(data['name']) < 3:
            errors.append("Name must be at least 3 characters long.")
        if not data['name'].isalpha():
            errors.append("Name may only be letters")
        if len(data['username']) < 3:
            errors.append("Username must be at least 3 characters long.")
        if data['e_address'] == '':
            errors.append("Email may not be blank")
        if not EMAIL_REGEX.match(data['e_address']):
            errors.append("Please enter a vailid email address")
        try:
            User.objects.get(email = data['e_address'])
            errors.append("Email is already registered, please log in.")
        except:
            pass
        if len(data['pass_word']) < 8:
            errors.append("Password must be at least 8 characters long.")
        if data['pass_word'] != data['confirm_pass_word']:
            errors.append("Password and confirm password does not match.")
        if len(errors) == 0:
            print('no errors')
            data['pass_word'] = bcrypt.hashpw(data['pass_word'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(name=data['name'], username=data['username'], email=data['e_address'], password=data['pass_word'])
            return {
                'new': new_user,
                'error_list': None,
            }
        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }
    def log(self, log_data):
        errors = []
        try:
            found_user = User.objects.get(email=log_data['e_mail'])
            if bcrypt.hashpw(log_data['p_word'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect Password.")
        except:
            errors.append("Email Address is not registered")
        if len(errors) == 0:
            return {
                'logged_user': found_user,
                'list_errors': None,
            }
        else:
            return {
                'logged_user': None,
                'list_errors': errors,
            }

class WishManager(models.Manager):
    def new(self, data):
        errors = []
        if len(data['item']) < 3:
            errors.append("Please enter the Item/product you are wishing for (must be at least 3 characters)")
        if len(errors) == 0:
            print('no errors')
            new_wish = Wish.objects.create(item=data['item'], creator=data['creator'])
            return {
                'new': new_wish,
                'error_list': None,
            }
        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors,
            }

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=100)
    creator = models.ForeignKey(User, related_name="wish_creater")
    users = models.ManyToManyField(User, related_name='wishers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = WishManager()
