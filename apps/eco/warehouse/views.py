from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Product

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = None
        return context

class ProductListByCategoryView(ProductListView):
    def get_queryset(self):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, translations__slug=slug)
        queryset = super().get_queryset()
        queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['category_slug']
        context['category'] = get_object_or_404(Category, translations__slug=slug)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

