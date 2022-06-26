from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from .models import Document, SecurePin, Address
from store.models import Store, StoreSetting, Order
from cryptography.fernet import Fernet
import os
import PyPDF2
from dotenv import load_dotenv
from django.conf import settings
import stripe
from django.views.generic.base import TemplateView
# import messages
from django.contrib import messages



load_dotenv()

# Create your views here.
@login_required
def index(req):
    context = {}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    if Document.objects.filter(user=req.user).exists():
        context['docs_available'] = True
        context['docs'] = Document.objects.filter(user=req.user)
    context['stores'] = Store.objects.all()
    store_settings = StoreSetting.objects.all()
    context['store_settings'] = store_settings
    return render(req, "main/index.html", context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, rate, order_id):
    if request.method == 'GET':
        domain_url = 'http://' + request.get_host() + '/'
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}&order=' + order_id,
                cancel_url=domain_url + 'cancelled/',
                mode='payment',
                line_items=[
                    {
                        'name': 'Document Print',
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': str(int(float(rate) * 100)),
                    }
                ]
            )
            return redirect(checkout_session['url'])
        except Exception as e:
            return JsonResponse({'error': str(e)})

def SuccessView(req):
    if req.method == "GET":
        order_id = req.GET['order']
        order = Order.objects.get(id=order_id)
        order.payment_status = "Paid"
        order.save()
        messages.success(req, 'Order Created Successfully')
    return render(req, 'main/payment_success.html')

def CancelledView(req):
    return render(req, 'main/payment_cancelled.html')

    # return stripe.redirectToCheckout({sessionId: session.id})

        

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
        messages.success(req, 'Document uploaded successfully')
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
                messages.success(req, 'Pin created successfully')
            else:
                messages.error(req, 'Pin not matched')
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    address = Address.objects.filter(user=req.user)
    context['address'] = address
    if Store.objects.filter(user=req.user).exists():
        store = Store.objects.get(user=req.user)
        store_settings = StoreSetting.objects.get(store=store)
        context['is_store'] = True
        context['store'] = store
        context['store_settings'] = store_settings
    return render(req, "main/settings.html", context)

def addAddress(req):
    if req.method == "POST":
        address = Address(user=req.user, area=req.POST['area'], distrcit=req.POST['district'], state=req.POST['state'], country=req.POST['country'], pincode=req.POST['pincode'])
        address.save()
        messages.success(req, 'Address added successfully')
    else:
        messages.error(req, 'Opps! Something went wrong')
    return redirect(to='settings')

def deleteAddr(req, id):
    address = Address.objects.get(id=id)
    address.delete()
    messages.success(req, 'Address deleted successfully')
    return redirect(to='settings')

def deleteDoc(req, id):
    doc = Document.objects.get(id=id)
    doc.delete()
    messages.success(req, 'Document deleted successfully')
    return redirect(to='yourdocs')

def getRates(req):
    if req.method =="GET":
        store = Store.objects.get(id=req.GET['store_id'])
        print_type = req.GET['print_type']
        store_setting = StoreSetting.objects.get(store=store)
        rate = store_setting.get_rate(print_type)
        return JsonResponse({'rate': rate})