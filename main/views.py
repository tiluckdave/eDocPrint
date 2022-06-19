from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document, SecurePin, Order, Address
from store.models import Store
from cryptography.fernet import Fernet
import os
import PyPDF2
from dotenv import load_dotenv
import razorpay
from django.conf import settings

load_dotenv()

# Create your views here.
@login_required
def index(req):
    
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    return render(req, "main/index.html", context)

def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(os.getenv('RZP_KEY_ID'), os.getenv('RZP_KEY_SECRET')))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "main/payment.html",
            {
                "callback_url": "http://" + request.META['HTTP_HOST'] + "/razorpay/callback/",
                "razorpay_key": os.getenv("RZP_KEY_ID"),
                "order": order,
            },
        )
    return render(request, "main/payment.html")

@login_required
def yourdocs(req):
    if req.method == "POST":
        key = os.getenv('PIN_KEY')
        f = Fernet(key)
        name = req.POST['name']
        file = req.FILES['file']
        readpdf = PyPDF2.PdfFileReader(file)
        totalpages = readpdf.numPages
        print(totalpages)
        doc = Document(name=name, document=file, pages=totalpages, prize=totalpages*2, user=req.user)
        doc.save()
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
    address = Address.objects.filter(user=req.user)
    context['address'] = address
    if Store.objects.filter(user=req.user).exists():
        context['store'] = True
    return render(req, "main/settings.html", context)

def addAddress(req):
    if req.method == "POST":
        address = Address(user=req.user, area=req.POST['area'], distrcit=req.POST['district'], state=req.POST['state'], country=req.POST['country'], pincode=req.POST['pincode'])
        address.save()
        return redirect(to='settings')
    return redirect(to='settings')

def deleteAddr(req, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect(to='settings')