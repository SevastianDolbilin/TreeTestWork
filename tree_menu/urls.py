from django.urls import path
from . import views

app_name = 'tree_menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<str:service_id>/', views.service_detail, name='service_detail'),
    path('products/', views.products, name='products'),
    path('products/<str:product_id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<str:post_id>/', views.blog_post, name='blog_post'),
    path('test/', views.test, name='test'),
] 