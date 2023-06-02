from django.db import models

# Create your models here.

class userInfo(models.Model):
    
    user_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    environment_score = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return {
            "user_id": self.user_id,
            "user_name" : self.user_name,
            "environment_score" : self.environment_score
        }