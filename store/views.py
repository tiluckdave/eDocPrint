from django.shortcuts import render, redirect
from main.models import Document, SecurePin, Address
from .models import Store

# Create your views here.
def registerStore(req):
    if req.method == "POST":
        addr = Address.objects.get(id=req.POST['address'])
        store = Store(user=req.user, Store_name=req.POST['name'], address=addr, Store_email=req.POST['email'], Store_phone=req.POST['phone'], Store_operator=req.POST['owner'])
        store.save()
        req.user.is_staff = True
        req.user.save()
        return redirect("index")
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    address = Address.objects.filter(user=req.user)
    context['address'] = address
    return render(req, "store/register-store.html", context)

def toggleStore(req):
    if req.user.is_staff:
        req.user.is_staff = False
    else:
        req.user.is_staff = True
    req.user.save()
    return redirect("settings")