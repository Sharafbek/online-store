from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from .models import Product, Category, Cart
from app_users.models import UserModel



class SearchData:
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search', '')
        if query and self.search_fields:
            search_queries = Q()
            for field in self.search_fields:
                search_queries |= Q(**{f"{field}__icontains": query})
            return queryset.filter(search_queries)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class CustomRangeForPagination:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        page_obj = context['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1
        
        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        return context


class ProductsView(SearchData, CustomRangeForPagination, ListView):
    template_name = 'app_main/products.html'
    context_object_name = 'products'
    search_fields = ['name', 'description']
    paginator_class = Paginator 
    paginate_by = 3

    
    def get_queryset(self):
        return Product.objects.all()
    


class CategoriesView(SearchData, CustomRangeForPagination, ListView):
    model = Category
    template_name = 'app_main/categories.html'
    context_object_name = 'categories'
    search_fields = ['name', 'description']
    paginator_class = Paginator
    paginate_by = 3


class ProductListByCategoryView(SearchData, CustomRangeForPagination, ListView):
    template_name = 'app_main/category.html'
    context_object_name = 'product_by_category'
    search_fields = ['name']
    paginate_by = 4                          

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            return Product.objects.filter(category=category).order_by('-id')
        return Product.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            context['category'] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_main/product_detail.html'
    context_object_name = 'product'


@login_required(login_url='login')
def add_to_cart(request, product_id):

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')


        try:
            cart = Cart.objects.create(
                product=get_object_or_404(Product, id=product_id),
                user=get_object_or_404(UserModel, id=request.user.id),
                quantity=quantity

            )
            cart.save()
        except:
            product = request.user.cart_set.all().get(product__id=product_id)
            product.quantity  += int(quantity)
            product.save()



    return redirect('product_detail', product_id=product_id)


@login_required(login_url='login')
def change_cart_product_quantity(request, cart_product_id, action):
    cart_product = get_object_or_404(Cart, id=cart_product_id)
    cart_product.quantity += 1 if action == "increment" else -1
    cart_product.save()
    return redirect('cart')    

