from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Author, Review
import re
import bcrypt

# Create your views here.
def index(request):
    return render(request, "manageuser/index.html")

def register(request):
    print "hello1"
    noerrors = False
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['password']
    hashedpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    pwconf = request.POST['pwconf']
    if(len(firstname)<3):
        noerrors = True
        messages.error(request, "First Name must be longer than 3 characters", extra_tags="firstname")
    if(len(lastname)<3):
        noerrors = True
        messages.error(request, "Last Name must be longer than 3 characters", extra_tags="lastname")
    if not EMAIL_REGEX.match(email):
        noerrors = True
        messages.error(request, "Must be a Valid Email", extra_tags = "email")
    if(len(password) < 8):
        noerrors = True
        messages.error(request, "Password must be longer than 8 characters", extra_tags ="password")
    if(password != pwconf):
        noerrors = True
        messages.error(request, "Your passwords do not match", extra_tags = "pwconf")
    if noerrors:
        print "hello"
        return redirect('/')
    else:
        newuser = User.objects.create(firstname=firstname, lastname=lastname, email = email, password = hashedpassword)
        newdict = {"id": newuser.id, "firstname" : newuser.firstname, "lastname": newuser.lastname, "email":newuser.email}
        request.session['user'] = newdict
        return redirect('/bookspage')

def login(request):
    email = request.POST['login_email']
    password = request.POST['login_password']
    user = User.objects.filter(email = email)
    usercheck = user[0]
    print usercheck.password
    if bcrypt.checkpw(password.encode(), usercheck.password.encode()):
        newdict = {"id": usercheck.id,"firstname" :usercheck.firstname, "lastname": usercheck.lastname, "email":usercheck.email}
        request.session['user'] = newdict
        return redirect('/bookspage')
    else:
        return redirect('/')

def bookspage(request):
    books = Book.objects.all().order_by('-id')[:3]
    reviews = Review.objects.all()
    newlist= []

    otherbooks = Book.objects.all()
    for book in otherbooks:

        if len(book.reviews.all()) > 0:
            newlist.append(book)
    
    context = {
        "books" : books,
        "reviews" : reviews,
        "bookswithreviews" : newlist
    }
    return render(request, 'manageuser/books.html', context)

def display_addbook(request):
    authors = Author.objects.all()
    context = {
        "authors" : authors
    }
    return render(request, 'manageuser/add.html', context)

def display_book(request, id):
    book = Book.objects.get(id=id)
    reviews = book.reviews.all()

    context = {
        "book" : book,
        "reviews" : reviews,

    }
    return render(request, 'manageuser/show.html', context)

def process_review(request, id):
    curruser = request.session['user']
    user = User.objects.get(id=curruser['id'])
    book = Book.objects.get(id=id)
    newreview = Review.objects.create(user = user, book = book)
    newreview.reviewdes = request.POST['reviewdescription']
    newreview.reviewrating = request.POST['rating']
    newreview.save()
    return redirect('/book/'+str(id))


def process_addbook(request):
    curruser = request.session['user']
    user = User.objects.get(id=curruser['id'])
    title = request.POST['booktitle']
    review = request.POST['reviewdescription']
    rating = request.POST['rating']
    if request.POST['newauthor']:
        author = request.POST['newauthor']
    else:
        author = request.POST['authorname']

    if type(author)==int:
        author_to_be_added = Author.objects.get(id=author)
    else:
        author_to_be_added = Author.objects.create()
        author_to_be_added.name = author
        author_to_be_added.save()
    newbook = Book.objects.create(title=title, author = author_to_be_added)
    newbook.save()
    if (review != ""):
        newreview = Review.objects.create(user = user, book = newbook)
        newreview.reviewdes = review
        newreview.reviewrating = rating
        newreview.save()
    return redirect('/book/'+str(newbook.id))


def display_user(request, id):
    user = User.objects.get(id=id)
    reviews = Review.objects.filter(user = user) 
    reviewcount = len(reviews)
    context = {
        "user" : user,
        "reviews" : reviews,
        "reviewcount" : reviewcount
    }
    return render(request, 'manageuser/user.html', context)

def remove(request):
    reviewid = request.POST['cancel']
    review_to_be_deleted = Review.objects.get(id = reviewid)
    review_to_be_deleted.delete()
    return redirect('/bookspage')



def logout(request):
    del request.session['user']
    return redirect('/')