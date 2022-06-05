import random

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from itertools import chain
from django.contrib.auth.decorators import login_required

from books.models import Book, Category

User = get_user_model()


# Home Page (home.html)
def home(request):
    context = {}
    books = Book.objects.all()

    random_num = random.randint(0, (len(books) - 1))
    random_book = books[random_num]
    context['book'] = random_book

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('books'))

        queries = Q(name__icontains=query) | Q(author__icontains=query)
        books = books.filter(queries)
        context = {
            'books': books,
            'search_term': query,
        }

        return render(request, 'books/books.html', context)

    return render(request, 'mindthereader/home.html', context)


# Login Page (login.html)
# => Page Aim :
# Allow registered users to login
# via standard form / social login (Facebook, Twitter, Google)
def signin(request):
    context = {}

    # Get username and password from user
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Check if username-password exists, and allow login if so
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successful login')
            return render(request, 'mindthereader/login.html', context=context)
        else:
            messages.error(request, 'Invalid login')
            return render(request, 'mindthereader/login.html', context=context)
    else:
        return render(request, 'mindthereader/login.html')


# Sign Up Page (signup.html)
# => Page Aim :
# Allow not registered users to sign up via
# standard form / social login (Facebook, Twitter, Google)
def signup(request):
    context = {}

    if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 == password2:
            username = request.POST['username']
            email = request.POST['email']

            # Check if username already exists
            try:
                user1 = User.objects.get(username=username)
                messages.error(request, 'Username is already in system')
                return render(request, 'mindthereader/signup.html', context=context)
            except User.DoesNotExist:
                # If username is unique, check if email already exists
                try:
                    user2 = User.objects.get(email=email)
                    messages.error(request, 'Email is already in system')
                    return render(request, 'mindthereader/signup.html', context=context)
                except User.DoesNotExist:
                    # If email and username are unique, create user
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=password1)
                    messages.success(request, "Thank you for signing up!")
                    return redirect('home')
        else:
            messages.error(request, 'Passwords must match')
            return render(request, 'mindthereader/signup.html', context=context)
    else:
        return render(request, 'mindthereader/signup.html')


# Logout Page (logout.html)
# => Page Aim :
# Allow already logged in users to logout
@login_required
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('mindthereader/logout.html')
