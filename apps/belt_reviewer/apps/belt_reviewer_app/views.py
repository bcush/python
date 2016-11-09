from django.shortcuts import render, redirect
from .models import User, Author, Book, Review
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'belt_reviewer_app/index.html')


def register(request):
    if request.method == 'POST':
        errors, user = User.objects.register(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, "Welcome {}!".format(user.alias))
            request.session['current_user'] = user.id
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
    return redirect('/books')


def logout(request):
    if 'current_user' in request.session:
        request.session.pop('current_user')
    return redirect('/')


def books(request):
    if 'current_user' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['current_user'])
    books = Book.objects.all()
    reviews = Review.objects.order_by('-created_at')

    context = {'user': user, 'books': books, 'reviews': reviews}
    return render(request, 'belt_reviewer_app/books.html', context)


def books_add(request):
    if 'current_user' not in request.session:
        redirect('/')
    user = User.objects.get(id=request.session['current_user'])
    authors = Author.objects.all()

    context = {'user': user, 'authors': authors}
    return render(request, 'belt_reviewer_app/books_add.html', context)


def books_id(request, id):
    if 'current_user' not in request.session:
        redirect('/')
    user = User.objects.get(id=request.session['current_user'])
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(book=book)
    context = {'user': user, 'book': book, 'reviews': reviews}
    return render(request, 'belt_reviewer_app/books_id.html', context)


def addbook(request):
    if 'current_user' not in request.session:
        redirect('/')

    # if 'author' in request.post:
    #     author = Author.objects.create(name=request.post['author'])

    book = Book.objects.addbook(request.POST)
    user = User.objects.get(id=request.session['current_user'])

    context = {'user': user, 'book': book}

    return redirect('/books')

def addrating(request):
    if 'current_user' not in request.session:
        return redirect('/')

    book = Book.objects.get(id=request.POST['book_id'])
    user = User.objects.get(id=request.session['current_user'])
    Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, user=user)

    return redirect('/books')

def users_id(request, id):
    if 'current_user' not in request.session:
        redirect('/')
    user = User.objects.get(id=id)
    reviews = Review.objects.filter(user=user)
    context = {'user': user, 'reviews': reviews}

    return render(request, 'belt_reviewer_app/users_id.html', context)
