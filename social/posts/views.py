from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group


def index(request):
    posts = Post.objects.all()[:11]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_posts = group.posts.all()[:13]
    context = {
        'group_posts': group_posts,
        'group': group,
    }
    return render(request, 'posts/group.html', context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Пост успешно добавлен!')
            return redirect('index')
        return render(request, 'posts/new_post.html', {'form':form})
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/new_post.html', context)
