from django.http import HttpResponse
from django.shortcuts import render
from .models import Blogpost



def index(request):
    return render(request,'blog/index.html')

def blogpost(request,id):
    try:
        post = Blogpost.objects.get(post_id=id)
         print(post)
            return render(request, 'blog/blogpost.html', {'post': post})
    except Blogpost.DoesNotExist:
            raise Http404("Blog post does not exist")


