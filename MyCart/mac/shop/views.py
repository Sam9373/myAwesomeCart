from django.http import HttpResponse
from django.shortcuts import render
from .models import Product,Contact
from math import ceil


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

def about(request):
    return render(request,'shop/about.html')

def contact(request):
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
    return render(request,'shop/contact.html')

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')

def productView(request,myid):
     # fetch the product using id
    product = Product.objects.filter(id=myid)
    # print(product)//
    return render(request,'shop/prodView.html',{'product':product[0]})

def checkout(request):
    return render(request,'shop/checkout.html')
