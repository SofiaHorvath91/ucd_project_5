import random

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from books.models import Book

User = get_user_model()


# Home Page (home.html)
# => Page Aim :
# Allow user to discover the
# main objective of site and available actions quickly
def home(request):
    context = {}
    all_books = Book.objects.all()

    # Get random book for recommendation
    if len(all_books) > 1:
        random_num = random.randint(0, (len(all_books) - 1))
        random_book = all_books[random_num]
        context['book'] = random_book

    # Allow users to use global search for books
    if 'q' in request.GET:
        query = request.GET['q']
        queries = global_search(request, query)
        books = all_books.filter(queries)
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

    # Allow users to use global search for books
    if 'q' in request.GET:
        query = request.GET['q']
        queries = global_search(request, query)
        books = Book.objects.filter(queries)
        context = {
            'books': books,
            'search_term': query,
        }
        return render(request, 'books/books.html', context)

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

    # Allow users to use global search for books
    if 'q' in request.GET:
        query = request.GET['q']
        queries = global_search(request, query)
        books = Book.objects.filter(queries)
        context = {
            'books': books,
            'search_term': query,
        }
        return render(request, 'books/books.html', context)

    # Handling registration request
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


# 404 Page (404.html)
# => Page Aim :
# Custom 404 page in case an entry is not found for better UX
def entry_not_found(request, exception, template_name='404.html'):
    return render(request, template_name)


# Helper methods

# Helper for global search
def global_search(request, query):
    if not query:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('books'))

    queries = Q(name__icontains=query) | Q(author__icontains=query)
    return queries