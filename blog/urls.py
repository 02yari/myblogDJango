from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view (template_name='blog/login.html', next_page='blog:post_list'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]