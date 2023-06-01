from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def index(request):
    
    if request.method == "GET":
        user_state = request.user.is_authenticated
        
        return render(
            request,
            "trashCan/index.html",
            {"user_state" : user_state}
        )
    
    elif request.method == "POST":
        
        forms = request.POST["user_id"]
        print(forms)
        
        return redirect("auth")

    
def login(request):
    return HttpResponse()