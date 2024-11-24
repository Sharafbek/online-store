from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from app_main.models import Cart
from .forms import UserRegistrationForm


User = get_user_model()


def account_func(request):
    context = {
        'search_button':True
    }
    return render(request=request,
                  template_name='app_users/account.html',
                  context=context)


class UserLogin(LoginView):
    template_name = 'app_users/login.html'


    def get_success_url(self):
        return self.request.POST.get('next')

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET' and request.user.is_authenticated:
            return redirect('products')
        
        return super().dispatch(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('login')


class UserRegistrationView(CreateView):
    template_name = 'app_users/registration.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET' and request.user.is_authenticated:
            return redirect('products')
        
        return super().dispatch(request, *args, **kwargs)


class CartView(ListView):
    template_name = 'app_users/cart.html'
    context_object_name = 'cart_products'
    

    def get_queryset(self):
        return self.request.user.cart_set.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_button'] = True
        return context
    

class CartProductDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart')
    pk_url_kwarg = 'cart_product_id'

