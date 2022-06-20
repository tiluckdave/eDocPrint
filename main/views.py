from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from .models import Document, SecurePin, Address
from store.models import Store
from cryptography.fernet import Fernet
import os
import PyPDF2
from dotenv import load_dotenv
from django.conf import settings
import stripe
from django.views.generic.base import TemplateView



load_dotenv()

# Create your views here.
@login_required
def index(req):
    
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    return render(req, "main/index.html", context)

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                mode='payment',
                line_items=[
                    {
                        'name': 'Document Print',
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': '100',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def SuccessView(req):
    return render(req, 'main/payment_success.html')

def CancelledView(req):
    return render(req, 'main/payment_cancelled.html')

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
        store = Store.objects.get(user=req.user)
        context['is_store'] = True
        context['store'] = store
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

def deleteDoc(req, id):
    doc = Document.objects.get(id=id)
    doc.delete()
    return redirect(to='yourdocs')