from django.db import models

class QRCode(models.Model):
    data = models.CharField(max_length=100)
    mobile_number = models.IntegerField(max_length=10)
    
    def __str__(self):
        return f"{self.data}-{self.mobile_number}"
    
class Scanner(models.Model):

    mobile_number = models.IntegerField(max_length=10)   
 
    def __str__(self):
        return f"{self.mobile_number}"