from django.shortcuts import render

from .models import Post


def index(request):
    posts = Post.objects.all()[:11]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)