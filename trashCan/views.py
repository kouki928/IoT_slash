from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import userInfo
from django.contrib.auth import authenticate, login, logout

# Create your views here.

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
            
            
            
def mypage(request):
    
    if request.method == "GET":
        
        user_id = request.user
        user = userInfo.objects.get(user_id=user_id)
        
        return render(request, "trashCan/mypage.html",{
            "user" : user
        })
        
    