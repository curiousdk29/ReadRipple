from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from pyuploadcare import Uploadcare

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'books/register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('browse_books')
    return render(request, 'books/login.html', {'form': form})

import os



uc = Uploadcare(public_key='2c71a577ee545662a068', secret_key='9baa96770ff55afa2572')

@login_required

def upload_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        age_group = request.POST['age_group']
        level = request.POST['level']
        file_uuid = request.POST['file']  # UUID from Uploadcare widget

        file_url = f"https://ucarecdn.com/{file_uuid}/"

        # Save book record
        Book.objects.create(
            title=title,
            description=description,
            age_group=age_group,
            level=level,
            file_url=file_url,
            file_uuid=file_uuid
        )

        return redirect('browse_books')

    return render(request, 'books/upload.html')



from django.contrib.auth.decorators import login_required

@login_required
def browse_books(request):
    age_group = request.GET.get('age_group')
    level = request.GET.get('level')
    books = Book.objects.all()
    if age_group:
        books = books.filter(age_group=age_group)
    if level:
        books = books.filter(level=level)
    return render(request, 'books/browse.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from .models import Book


# books/views.py

from .models import ReadingExercise

def exercise_list(request):
    exercises = ReadingExercise.objects.all()
    return render(request, 'books/exercise_list.html', {'exercises': exercises})

@login_required
def upload_exercise(request):
    if not request.user.is_staff:
        return redirect('browse_books')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            ReadingExercise.objects.create(title=title, content=content)
            return redirect('exercise_list')
    return render(request, 'books/upload_exercise.html')

from django.conf import settings

uploadcare = Uploadcare(public_key=settings.UPLOADCARE['pub_key'],
                        secret_key=settings.UPLOADCARE['secret'])




@login_required
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)

    # Delete from Uploadcare
    uploadcare.file(book.file_uuid).delete()

    # Delete from DB
    book.delete()

    return redirect('browse_books')

@login_required
def delete_exercise(request, exercise_id):
    if not request.user.is_staff:
        return redirect('browse_books')
    exercise = get_object_or_404(ReadingExercise, id=exercise_id)
    exercise.delete()
    return redirect('exercise_list')
