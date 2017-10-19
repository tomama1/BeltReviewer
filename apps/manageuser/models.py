from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255, default="000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "<User: {}{} {}>".format(self.firstname,self.lastname,self.created_at)

class Author(models.Model):
    name = models.CharField(max_length=50, default="0000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "<Author: {} {}>".format(self.name,self.created_at)


class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "<Book: {} {} {}>".format(self.title, self.author, self.created_at)


class Review(models.Model):
    reviewdes = models.TextField()
    reviewrating = models.SmallIntegerField(default=0)
    book = models.ForeignKey(Book, on_delete=None, related_name="reviews")
    user = models.ForeignKey(User, on_delete=None, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "<Review: {} {} {}>".format(self.book, self.user, self.created_at)
