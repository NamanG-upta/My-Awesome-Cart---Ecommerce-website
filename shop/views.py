from django.shortcuts import render
from .models import product, Contact, orders, ORDERSUPDATES
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
from django.http import HttpResponse

# MERCHANT_KEY = 'kbzk1DSbJiV_03p5';

def index(request):
    # prod = product.objects.all()
    # print(prod)
    # n = len(prod)
    # nslides = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides': nslides, 'range': range(1, nslides), 'product': prod}
    # nakli allprods only for testing
    # allprod = [[prod,range(1, nslides), nslides], [prod,range(1, nslides), nslides]]
    allprod = []
    catprod = product.objects.values('category', 'id')
    catg = {item['category'] for item in catprod}
    for cat in catg:
        pdt = product.objects.filter(category=cat)
        n = len(pdt)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprod.append([pdt, range(1, nslides), nslides])
    params = {'allprod': allprod}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item searched'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprod = []
    catprod = product.objects.values('category', 'id')
    catg = {item['category'] for item in catprod}
    for cat in catg:
        pdttemp = product.objects.filter(category=cat)
        pdt = [item for item in pdttemp if searchMatch(query , item)]
        n = len(pdt)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(pdt)!=0:
            allprod.append([pdt, range(1, nslides), nslides])
    params = {'allprod': allprod, "msg":""}
    if len(allprod) == 0 or len(query)<4:
        params = {'msg':"Please make sure that you enter relevant search query"}

    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')    
        try:
            order = orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = ORDERSUPDATES.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response=json.dumps({"status": "success", "updates": updates, "itemsJson" : order[0].items_json}, default= str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"no item"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')

def productview(request, myid):
    produ = product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'produ':produ[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount = amount)
        order.save()
        update = ORDERSUPDATES(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html',{'thank':thank, 'id': id})
        #request apytm to transfer amount to your account
        param_dict = {

                'MID': 'VMLsKh33374131769871',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})


    
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    #paytm will sent your post request
    return HttpResponse('done')
    pass