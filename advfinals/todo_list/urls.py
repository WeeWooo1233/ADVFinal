from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('delete/<int:item_id>/', views.delete, name='delete'),
    path('crossoff/<int:item_id>/', views.cross_off, name='cross_off'),
    path('uncross/<int:item_id>/', views.uncross, name='uncross'),
    path('edit/<int:item_id>/', views.edit, name='edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),  # login without 'accounts/'
    path('logout/', views.user_logout, name='logout'),  # logout without 'accounts/'
]
