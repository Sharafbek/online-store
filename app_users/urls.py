from django.urls import path
from django.contrib.auth.views import LoginView


from . import views


urlpatterns = [

    path('login/', LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),

    path('account/', views.account_func, name='account'),

    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart-product-delete/<int:cart_product_id>/', views.CartProductDeleteView.as_view(), name='cart_product_delete'),    

]   

