from django.http import HttpResponse
from django.shortcuts import render
from .models import Blogpost



def index(request):
    myposts=Blogpost.objects.all()
    print(myposts)
    return render(request,'blog/index.html',{'myposts':myposts})

def blogpost(request,id):
    try:
        post = Blogpost.objects.get(post_id=id)
        print(post)
        return render(request, 'blog/blogpost.html', {'post': post})
    except Blogpost.DoesNotExist:
        raise Http404("Blog post does not exist")


