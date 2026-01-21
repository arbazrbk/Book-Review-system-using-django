from django.shortcuts import render,redirect
from .forms import BookForm
from django.views import View
from django.views.generic import templateview,redirectview
from .models import Book

class BookCreatedView(View):
    def get(self,request):
        form = BookForm()
        return render(request,'book/book_create.html',{'form':form})
    
    def post(self,request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book:create')
        
class BookListView(View):
    Template_name = 'book/book_list.html'
    
class BookDetailView(BookListView):
    Template_name = 'book/book_detail.html'
    
class BookUpdateView(BookListView):
    def get(self,request,pk):
        form = BookForm()
        return render(request,'book/book_update.html',{'form':form})

class BookDeleteView(redirectview):
    pattern_name = 'book:list'      
    
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        messages.get(self.request, 'Book deleted successfully.')
        return super().get_redirect_url(*args, **kwargs)