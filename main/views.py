from django.shortcuts import render, redirect

# Create your views here.
def index(req):
    if req.user.is_authenticated:
        return render(req, "main/index.html")
    else:
        return redirect(to='magiclink:login')