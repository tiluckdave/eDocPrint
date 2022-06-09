from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document, SecurePin
from cryptography.fernet import Fernet

# Create your views here.
@login_required
def index(req):
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    return render(req, "main/index.html", context)

@login_required
def yourdocs(req):
    if req.method == "POST":
        encpin = SecurePin.objects.get(user=req.user).pin
        # key = b'QUjJWtykXCB8TTL2jS8BPHDZQbp4yU65gGhokr_lED8='
        # key = bytes(encpin[2:46], 'Base64')
        # print(key)
        fernet = Fernet(key)
        # file = req.FILES['file']
        # encfile = f.encrypt(file)
        # doc = Document(name="ABC", document=file, user=req.user)
        # doc.save()
    docs = Document.objects.filter(user=req.user) 
    context = {'spin':False, 'docs':docs}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    return render(req, "main/yourdocs.html", context)

@login_required()
def settings(req):
    if req.method == "POST":
        if req.POST['pin'] == "":
            return redirect('main:settings')
        else:
            if req.POST['pin'] == req.POST['confpin']:
                pin = SecurePin(user=req.user, pin=req.POST['pin'].encode())
                pin.save()
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    return render(req, "main/settings.html", context)