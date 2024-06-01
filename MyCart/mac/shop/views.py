from django.http import HttpResponse
from django.shortcuts import render
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
# from .paytm import generate_checksum
# MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


def index(request):
    products=Product.objects.all()
    # print("All Products:")
    # for product in products:
    #     print("ID:", product.id)
    #     print("Name:", product.product_name)
    #     print("Category:", product.category)
    #     print("Subcategory:", product.subcategory)
    #     print("Price:", product.price)
    #     print("Description:", product.desc)
    #     print("Publication Date:", product.pub_date)
    #     print("Image:", product.image.url if product.image else "No image")
    #     print("------------------------------")

    # for creating another carousel

    # n= len(products)
    # nSlides = n//4 + ceil((n/4) - (n//4))
    # params={'No_of_slides':nSlides,'range':range(1,nSlides),'Products':products}
    # # params = {'No_of_slides':nSlides,"products":products,'range':range(1,nSlides)}
    # allProds=[[products,range(1,nSlides),nSlides],
    #           [products,range(1,nSlides),nSlides]]
    # products = Product.objects.all()

    # For accessing categories for each product and displaying product according to category

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request,'shop/indexOriginal.html',params)

def searchMatch(query,item):
    '''return true only if the query matches the item '''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!=0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds,'msg':""}
    # '''if we sesrch with any character other thsn related to products'''
    if len(allProds)==0 or  len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}

    return render(request, 'shop/search.html', params)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank=False
    if request.method == "POST":
        print(request)
        name=request.POST.get('name','')
        # print(name)
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
    return render(request,'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({"status":"success","updates":"updates","itemsJson": order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')


    return render(request,'shop/tracker.html')



def productView(request,myid):
     # fetch the product using id
    product = Product.objects.filter(id=myid)
    # print(product)//
    return render(request,'shop/prodView.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        print(request)
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount = request.POST.get('amount', '')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+ " " + request.POST.get('address2','')
        city=request.POST.get('city','')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order=Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        #when order is placed it will give update msg
        update=OrderUpdate(order_id=order.order_id,update_desc="Your order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request,'shop/checkout.html',{'thank':thank ,'id':id})
    # req payment to transfer the amount to account after payment by user
        param_dict = {

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

         }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})

    return render(request,'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post req here
    return HttpResponse('Done')
    pass