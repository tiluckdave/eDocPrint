from django.shortcuts import render, redirect
from main.models import Document, SecurePin, Address
from .models import Store, StoreSetting, Order
from main.views import create_checkout_session
from django.contrib import messages

# Create your views here.
def orders(req):
    context = {}
    if req.user.is_staff:
        store = Store.objects.get(user=req.user)
        orders = Order.objects.filter(store=store)
        context['orders'] = orders
    else:
        orders = Order.objects.filter(user=req.user)
        context['orders'] = orders
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    return render(req, "store/orders.html", context)


def registerStore(req):
    if req.method == "POST":
        addr = Address.objects.get(id=req.POST['address'])
        store = Store(user=req.user, Store_name=req.POST['name'], address=addr, Store_email=req.POST['email'], Store_phone=req.POST['phone'], Store_operator=req.POST['owner'])
        store.save()
        messages.success(req, "Store Registered Successfully")
        store_settings = StoreSetting(store=store)
        store_settings.save()
        messages.success(req, "Please wait untill verified by admin")
        return redirect("index")
    context = {'spin':False}
    if SecurePin.objects.filter(user=req.user).exists():
        context['spin'] = True
    address = Address.objects.filter(user=req.user)
    context['address'] = address
    return render(req, "store/register-store.html", context)

def dashboard(req):
    context = {}
    store = Store.objects.get(user=req.user)
    orders = Order.objects.filter(store=store, payment_mode="card")
    tostore = 0
    for order in orders:
        tostore += order.tostore_rate
    context['store'] = store
    context['tostore_rate'] = tostore
    return render(req, "store/dashboard.html", context)

def updateStoreDetails(req):
    if req.method == "POST":
        store = Store.objects.get(user=req.user)
        store.Store_name = req.POST['name']
        store.Store_email = req.POST['email']
        store.Store_phone = req.POST['phone']
        store.Store_operator = req.POST['owner']
        store.save()
        messages.success(req, "Store Details Updated Successfully")
    return redirect('settings')

def updateStoreRates(req):
    if req.method == "POST":
        store = Store.objects.get(user=req.user)
        store_settings = StoreSetting.objects.get(store=store)
        store_settings.bnw_one_side_rate = req.POST['bnw_one_side_rate']
        store_settings.bnw_two_side_rate = req.POST['bnw_two_side_rate']
        store_settings.color_one_side_rate = req.POST['color_one_side_rate']
        store_settings.color_two_side_rate = req.POST['color_two_side_rate']
        store_settings.photo_4x6_rate = req.POST['photo_4x6_rate']
        store_settings.photo_A4_rate = req.POST['photo_A4_rate']
        store_settings.save()
        messages.success(req, "Store Rates Updated Successfully")
    return redirect('settings')

def get_print_type(pt):
    if pt == "bo":
        return "Black and White One Side"
    elif pt == "bt":
        return "Black and White Two Side"
    elif pt == "co": 
        return "Color One Side"
    elif pt == "ct":
        return "Color Two Side"
    elif pt == "ps":
        return "Photo 4x6"
    elif pt == "pl":
        return "Photo A4"
        
def createOrder(req):
    if req.method == "POST":
        user = req.user
        store = Store.objects.get(id=req.POST['store'])
        document = Document.objects.get(id=req.POST['document'].split(',')[1])
        print_type = get_print_type(req.POST['print_type'])
        rate = req.POST['rate']
        total = req.POST['total']
        payment_mode = req.POST['payment_mode']
        order = Order(user=user, store=store, document=document, print_type=print_type, rate=rate, tostore_rate=total, payment_mode=payment_mode, payment_status="Pending")
        order.save()
        messages.success(req, "Order Created Successfully")
        if payment_mode == "cash":
            return redirect("index")
        return redirect(create_checkout_session, rate, order.id)
    return redirect("index")

def deleteOrder(req, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.success(req, "Order Deleted Successfully")
    return redirect('orders')

def paidOrder(req, id):
    order = Order.objects.get(id=id)
    order.payment_status = "Paid"
    order.save()
    messages.success(req, "Order Paid!")
    return redirect('orders')


def toggleStore(req):
    if req.user.is_staff:
        req.user.is_staff = False
        messages.success(req, "Logged out as Store")
    else:
        req.user.is_staff = True
        messages.success(req, "Logged in as Store")
    req.user.save()
    return redirect("settings")