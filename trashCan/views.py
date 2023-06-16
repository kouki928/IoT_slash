from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import userInfo,userNotice
from django.contrib.auth import authenticate, login, logout
from django.core.mail import BadHeaderError, send_mail

# Create your views here.

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    
    if request.method == "GET":
        
        user_state = request.user.is_authenticated
        
        # index.html を描写 ---------------------------- #
        return render(
            request,
            "trashCan/index.html",
            {
                "user_state" : user_state,
                "error" : False
            }
        )
    
    
    elif request.method == "POST":
        
        forms = request.POST
        
        if forms["inout"] == "logout":
            logout(request)
            return redirect("auth")
        
        user_id = forms["user_id"]
        password = forms["password"]

        user = authenticate(request, username=user_id, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("auth")
        
        else:
            return render(request,"trashCan/index.html",{
                "user_state" : False,
                "error" : True,
                "user_id" : user_id,
                "password" : password,
            })

    
def signUp(request):
    
    if request.method == "GET":

        # signUp.html を描写 ---------------------------- #
        return render(
            request,
            "trashCan/signUp.html",
            {
                "error" : False,
            }
        )
    
    elif request.method == "POST":
        forms = request.POST
        user_id = forms["user_id"]
        password = forms["password"]
        
        try:
            existing_user = User.objects.get(username=user_id)
            
            return render(request, "trashCan/signUp.html",{
                "user" : existing_user,
                "error" : True
            })
            
        except:
        
            User.objects.create_user(username=user_id,password=password)
            userInfo.objects.create(user_id=user_id, user_name="未設定", environment_score=0)
            user = authenticate(request, username=user_id, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("auth")
            
            else:
                return HttpResponse("Error")
            
            
@csrf_exempt            
def mypage(request):
    
    user_id = request.user
    user = userInfo.objects.get(user_id=user_id)
    
    if request.method == "GET":
        
        return render(request, "trashCan/mypage.html",{
            "user" : user,
            "edit" : False
        })
    
    elif request.method == "POST" and request.POST["edit"] == "transition":
        
        return render(request, "trashCan/mypage.html",{
            "user" : user,
            "edit" : True
        })
        
    elif request.method == "POST" and request.POST["edit"] == "edit":
        
        user_name = request.POST["user_name"]
        
        if user_name.split() == []:
            user_name = "未設定"
        
        user.user_name = user_name
            
        user.save()
        
        return redirect("mypage")
    
    elif request.method == "POST" and request.POST["edit"] == "back":
        
        return redirect("mypage")
    

@csrf_exempt
def points(request):
    
    if request.method == "GET":
        return render(request, "trashCan/points.html",{})
    

@csrf_exempt
def notice(request):
    
    if request.method == "GET":
        
        user_id = request.user
        notice_data = userNotice.objects.filter(user_id=user_id).values()
        user_notice = []
        
        for data in notice_data:
            user_notice.append({
                "title" : data["title"],
                "body"  : data["body"]
            })
        
        return render(request, "trashCan/notice.html",{
            "notice" : user_notice,
            "notification" : user_notice if user_notice else False
        })
    
    

@csrf_exempt 
def send_email(request):
    
    if request.method == "POST":
        
        subject = "ゴミ箱が一杯です！"
        message = "ゴミ箱が一杯になりそうです。ゴミ袋を取り替えて下さい。"
        from_email = "information@myproject"
        recipient_list = [
            "koukifurukawa0625@gmail.com"
        ]

        send_mail(subject, message, from_email, recipient_list)
        
        return HttpResponse()

    elif request.method == "GET":
        print("通知が来たよ！")
        return HttpResponse()