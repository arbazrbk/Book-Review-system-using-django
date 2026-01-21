from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import BookForm
from django.views import View
from django.views.generic import TemplateView, RedirectView
from .models import Book

class BookCreatedView(View):
    def get(self,request):
        form = BookForm()
        return render(request,'book/book_form.html',{'form':form})
    
    def post(self,request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Book added successfully.')
            return redirect('list')
        return render(request,'book/book_form.html',{'form':form})
        
class BookListView(TemplateView):
    template_name = 'book/book_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all().order_by('published_date')
        return context
    
class BookDetailView(View):
    template_name = 'book/book_detail.html'
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, self.template_name, {'book': book})
    
    def post(self,request, pk):
        pass
    
class BookUpdateView(BookListView):
    def get(self,request,pk):
        book = Book.objects.get(pk=pk)
        form = BookForm(instance=book)
        return render(request,'book/book_update.html',{'form':form})
    
    def post(self,request,pk):
        book = Book.objects.get(pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('update',pk=pk)
        return render(request,'book/book_update.html',{'form':form})

    