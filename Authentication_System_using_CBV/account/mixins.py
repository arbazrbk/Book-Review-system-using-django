from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.http import HttResponseForbidden


class MixinClass(UserPassesTestMixin):
    def test_fun(self):
        return  self.user.request.user.is_authenticated and hasattr(self.request.user,'is_customer')
        and self.request.user.is_customer
    
    
    def handel_no_permission(self):
        if self.user.is_authenticated:
           return HttResponseForbidden("acess_denned")
        
        return redirect('login')
    
    
    def test_fun(self):
        return  self.user.request.user.is_authenticated and hasattr(self.request.user,'is_seller')
        and self.request.user.is_seller
    
    
    def handel_no_permission(self):
        if self.user.is_authenticated:
           return HttResponseForbidden("acess_denned")
        
        return redirect('login')    