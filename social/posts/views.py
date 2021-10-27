from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Follow


@cache_page(20)
def index(request):
    post_list = Post.objects.select_related('author', 'group').prefetch_related('comments__post').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'posts': post_list,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date').select_related('author').prefetch_related('comments__post').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group,
        'page': page,
        'paginator': paginator,
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
        return render(request, 'posts/post_new.html', {'form':form})
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_new.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related('author', 'group').prefetch_related('comments__post').filter(author__username=username).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = Follow.objects.filter(author=user, user=request.user).exists()
    context = {
        'user': user,
        'page': page,
        'paginator': paginator,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)

    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post', username, post_id)

    context = {
        'post': post,
        'form': form,
        'items': post.comments.all(),
    }
    return render(request, 'posts/post.html', context)


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user.username != username:
        return redirect('post', username, post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username, post_id)

    context = {
        'form': form,
        'post': post,
        'edit': True,
    }
    return render(request, 'posts/post_new.html', context)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()
            return redirect('post', username, post_id)

    context = {
        'form': form,
        'post': post,
        'items': post.comments.all(),
    }
    return render(request, 'posts/post.html', context)


@cache_page(20)
@login_required
def follow_index(request):
    user = request.user
    follower_list = Follow.objects.filter(user=user)
    post_list = Post.objects.select_related('author','group').prefetch_related('comments__post').filter(author__in=User.objects.filter(following__in=follower_list))
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)

    Follow.objects.create(
        user=user,
        author=author
    )

    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)

    Follow.objects.filter(user=user, author=author).delete()

    return redirect('profile', username=username)