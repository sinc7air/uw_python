from django.db import models

class Book(models.Model):
    ident = models.CharField(max_length=7)
    title = models.CharField(max_length = 255)
    isbn = models.CharField(max_length = 15)
    publisher = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title

# Create your models here.
