from django.http import Http404
from django.shortcuts import render
from datetime import datetime as dt
from django.conf import settings
from .models import *
# Create your views here.


def index(request):
    import os
    # List of JavaScript filenames
    # Path to your static folder
    static_folder = os.path.join(settings.BASE_DIR, "static")

    # List of JavaScript filenames from the static folder
    js_files = [f for f in os.listdir(static_folder) if f.endswith('.js')]
    # print(js_files)
    context = {
        "js_files": js_files,
    }
    return render(request, 'main.html', context)


def home(request):
    # info = SiteInformation.objects.all()
    # if len(info) != 1:
    #     raise Http404('Information for this site is not posted.')
    # info = info[0]

    services = Service.objects.all()
    projects = Project.objects.filter(is_published=True).order_by('-modified')
    features = Feature.objects.all()
    offerings = Offering.objects.all()
    marketings = Marketing.objects.all()
    teammembers = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        # 'site_information': info,
        'services': services,
        'projects': projects,
        'features': features,
        'offerings': offerings,
        'marketings': marketings,
        'teammembers': teammembers,
        'testimonials': testimonials,
        'copyright': f'2000-{dt.now().year}',	
    }
    return render(request, 'main.html', context)





# from django.views.generic import ListView
# from django.views.generic import DetailView
# from .models import Category, Post


# def blog(request):
#     categories = Category.objects.all()
#     posts = Post.objects.all()

#     context = {
#         'categories': categories,
#         'posts': posts,
#     }
#     return render(request, 'blog/blogs.html', context)



# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'  # Create this template
#     context_object_name = 'posts'
#     ordering = ['-created_at']
#     paginate_by = 10  # Adjust as needed


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'  # Create this template
#     context_object_name = 'post'


# class CategoryListView(ListView):
#     model = Category
#     template_name = 'blog/category_list.html'  # Create this template
#     context_object_name = 'categories'


# class CategoryDetailView(ListView):
#     template_name = 'blog/category_detail.html'  # Create this template
#     context_object_name = 'category_posts'
#     paginate_by = 10  # Adjust as needed

#     def get_queryset(self):
#         category = Category.objects.get(slug=self.kwargs['slug'])
#         return Post.objects.filter(categories=category).order_by('-created_at')


# def bootstrap(request):
# 	context = {
# 	}
# 	return render(request, 'bootstrap.html', context)