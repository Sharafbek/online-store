from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductsView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('change-cart-product-quantity/<int:cart_product_id>/<str:action>/', views.change_cart_product_quantity, name='change_cart_product_quantity'),


    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('products/<int:category_id>/', views.ProductListByCategoryView.as_view(), name='product_list'),


]