"""
URL configuration for PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import (PasswordResetView, 
                                       PasswordResetDoneView, 
                                       PasswordResetConfirmView, 
                                       PasswordResetCompleteView)

from django.conf import settings
from django .conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('app_main.urls')),

    path('users/', include('app_users.urls')),


    path('social-auth/', include('social_django.urls', namespace='social')),


    path('password-reset/', PasswordResetView.as_view(template_name='app_users/password-reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='app_users/password-reset-done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='app_users/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='app_users/password-reset-complete.html'), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)

