from __future__ import unicode_literals

from django.db import models

import re, bcrypt

emailre = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    """ A custom object manager for User """
    def register(self, form_data):
        errors = []
        if len(form_data['name']) == 0:
            errors.append('Name must not be blank.')
        if len(form_data['alias']) == 0:
            errors.append('Alias must not be blank.')
        if not emailre.match(form_data['email']):
            errors.append('Email is not valid.')
        if len(form_data['password']) < 8:
            errors.append('Password is less than 8 characters.')
        if form_data['password'] != form_data['passconf']:
            errors.append('Passwords do not match.')
        if len(form_data['dob']) == 0:
            errors.append('Date of birth cannot be blank.')
        # else:
        #     try:
        #         today = datetime.now()
        #         print today
        #         date = datetime.strptime(form_data['dob'], "%Y-%m-%d")
        #         print date
        #         if date > today:
        #             errors.append('Date of birth is invalid.')
        #     except:
        #         errors.append('Please provide a valid date of birth.')
        if len(errors) > 0:
            return (errors, None)
        if len(errors) == 0:
            encoded_password = form_data['password'].encode()
            pw_hash = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            user = User.objects.create(name=form_data['name'],
                                        alias=form_data['alias'],
                                        email=form_data['email'],
                                        password = pw_hash,
                                        dob = form_data['dob'])
            if not user:
                return (['An error has occured.'], None)

            return (None, user)

    def login(self, form_data):
        errors = []
        check_email = User.objects.filter(email=form_data['email'])
        if len(check_email) > 0:
            user = check_email[0]
            if bcrypt.hashpw(form_data['password'].encode(), user.password.encode()) == user.password:
                return (None, user)
        errors.append('Invalid credentials.')
        return (errors, None)

class User(models.Model):
    """ A representation of a User """
    name = models.CharField(max_length=80)
    alias = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=250)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name="friendship_through_user")
    friend = models.ForeignKey(User, related_name="friendship_through_friend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)