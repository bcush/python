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


class BookManager(models.Manager):
    """ A custom object manager for User """
    def addbook(request, postdata):
        if postdata['author']:
            print 'author in postdata'
            author = Author.objects.create(name=postdata['author'])
        if postdata['author_id']:
            print 'author_id is in postdata'
            print postdata
            author = Author.objects.get(id=postdata['author_id'])

        book = Book.objects.create(title=postdata['title'], author=author)
        user = User.objects.get(id=postdata['user_id'])

        post_review = postdata['review']
        if len(post_review) > 0:
            Review.objects.create(review=postdata['review'], rating=postdata['rating'], book=book, user=user)
        return book


class User(models.Model):
    """ A representation of a user """
    name = models.CharField(max_length=80)
    alias = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=250)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    """ A representation of an author """
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    """ A representation of a book """
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    """ A representation of a review for a book """
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "created_at"
