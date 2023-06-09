from django.db import models

# Create your models here.

class userInfo(models.Model):
    
    user_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    environment_score = models.DecimalField(max_digits=10,decimal_places=2)
    
        
        
        
class userNotice(models.Model):
    
    user_id = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=400)