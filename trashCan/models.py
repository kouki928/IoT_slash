from django.db import models

# Create your models here.

class userInfo(models.Model):
    
    # 商品ID
    user_id = models.CharField(max_length=200)
    
    # ユーザーの名前
    user_name = models.CharField(max_length=200)
    
    # スコア
    environment_score = models.DecimalField(max_digits=10,decimal_places=2)
    
    # LINE_ID
    line_id = models.CharField(max_length=100)
    
        
        
        
class userNotice(models.Model):
    
    user_id = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=400)