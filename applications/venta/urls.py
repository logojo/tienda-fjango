from django.urls import path

from . import views

app_name='sales_app'

urlpatterns = [
    path('api/sales', views.SalesReport.as_view(), name='sales'),
    path('api/sale', views.SaleView.as_view(), name='sale'),
     path('api/sale-custom', views.SaleCustomView.as_view(), name='sale-custom'),
]