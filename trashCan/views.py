from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    
    if request.method == "GET":
        
        user_state = request.user.is_authenticated
        print(user_state)
        # index.html を描写 ---------------------------- #
        return render(
            request,
            "trashCan/index.html",
            {
                "user_state" : user_state
            }
        )
    
    
    elif request.method == "POST":
        
        forms = request.POST
        user_state = forms["user_state"]
        user_id = forms["user_id"]
        password = forms["password"]

        user = authenticate(request, username=user_id, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("auth")
        
        else:
            return HttpResponse("Error")

    
def signUp(request):
    
    if request.method == "GET":

        # signUp.html を描写 ---------------------------- #
        return render(
            request,
            "trashCan/signUp.html",
        )
    
    elif request.method == "POST":
        forms = request.POST
        user_id = forms["user_id"]
        password = forms["password"]
        
        User.objects.create_user(username=user_id,password=password)
        user = authenticate(request, username=user_id, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("auth")
        
        else:
            return HttpResponse("Error")