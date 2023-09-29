from django.urls import path

from . import views

app_name='products_app'

urlpatterns = [
    #path('api/products', views.ProductView.as_view(), name='products'),
    path('api/products-stock', views.ProductStockView.as_view(), name='products-stock'),
    path('api/products-genero/<gender>', views.ProductGeneroView.as_view(), name='products-genero'),
    path('api/products-filters/', views.ProductFiltersView.as_view(), name='products-filters'),
]