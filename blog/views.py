from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import CommentForm, ProfileForm, SignUpForm

def post_list(request):
    """Vista para mostrar la lista de posts publicados"""
    posts = Post.objects.filter(published=True).order_by('-published_date')
    
    # Paginación
    paginator = Paginator(posts, 5)  # 5 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, slug):
    """Vista para mostrar un post específico con sus comentarios"""
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Crear comentario pero no guardarlo aún
            new_comment = comment_form.save(commit=False)
            # Asignar el post actual al comentario
            new_comment.post = post
            # Guardar el comentario
            new_comment.save()
            messages.success(request, '¡Tu comentario ha sido añadido exitosamente!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('blog:login')
        else:
            print("Form errors:", form.errors)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {'form': form})