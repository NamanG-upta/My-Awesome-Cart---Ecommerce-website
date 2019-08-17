from django.shortcuts import render

from .models import Blogpost


def index(request):
	myposts = Blogpost.objects.all()
	print(myposts)
	return render(request,'blog/index.html', {'myposts': myposts})

def blogpost(request, myyid):
	post = Blogpost.objects.filter(post_id = myyid)[0]
	print(post)
	return render(request, 'blog/blogpost.html', {'post':post})
