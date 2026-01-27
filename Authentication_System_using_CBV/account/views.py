from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from account.forms import RegistrationForm
from django.utils.http import urlsafe_base64_encode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate,logout
from account.models import User
from django.contrib import messages
from django import forms 
from django.shortcuts import redirect
from account.mixins import MixinClass



class loginView(View,MixinClass):
    def get(self,request,*args,**kwargs):
        return render (request, 'account/login.html')
    
    def post(self,request,*args,**kwargs):
        #form = RegistrationForm(request.POST)
        
       # if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email,password)
        
           
            if not password or not email :
                raise ValueError ("please provide both email and password")
        
        
            user = authenticate(request,email=email,password=password)
            try :
                
               user = User.objects.get(email = email )
                
            except User.DoesNotExist:
                messages.error(request,"invalid email or password")
                
            except password.DoesNotExist:
                messages.error(request,"invalid email or password")
                
                
                    
                return redirect('login') 
        
            if user.is_seller:
                return render(request, 'seller/dashboard.html') 
        
            elif user.is_customer:
                return render(request, 'customer/dashboard.html') 
          
            else:
                messages.error("you dont have the permission ")
                    
    
class RegistrationView(View,MixinClass):
    def get(self,request):
        form = RegistrationForm()
        return render (request, 'account/register.html',{'form':form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
           # user = form.save(commit=False)
           # user.set_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return render(request, 'account/login.html')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            return render(request, 'account/register.html', {'form': form})
        
        
        #uid56 = urlsafe_base64_encode(force_bytes(user.pk))
       # token = default_token_generator.make_token(user)
        
       # activation_link = reverse("activate",kwarge = {'uid56':uid56,'token':token})
       # activation_url = f'(settings.SITE_DOAMIN)'{activation_link}
        
class PasswordChangedView(PasswordChangeView, MixinClass):
    template_name = 'customer/change_password.html'
    sucess_url = reverse_lazy('dashboard')
    
    def is_valid(self,form):
        form.save()
        logout(self.request)
        messages.sucess(self.request,"your password has been changed successfully please login again")
        return super().is_valid(form)
    
    def not_valid(self,form):
        messages.error (self.request,"there was an error updating your password")
        return super().not_valid(form)        
    
class HomeView(View, MixinClass):
    def get(self,request,*args,**kwargs):
        return render (request, 'account/home.html')