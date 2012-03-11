# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response,get_object_or_404
from books.models import Book

def index(request):
    latest_book_list = Book.objects.all()
    t=loader.get_template('books/index.html')
    c=Context({'latest_book_list':latest_book_list,})
    return HttpResponse(t.render(c))

def detail(request, ident):
    p = get_object_or_404(Book,pk=(int(ident)))
    return render_to_response('books/detail.html',{'book':p})

