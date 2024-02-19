from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='index'),

    
    # path('bootstrap', views.bootstrap, name='bootstrap'),
    # # Blog Site
    # path('blogs', views.blog, name='blogs'),
    # path('blog', PostListView.as_view(), name='post-list'),
    # path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),


]

