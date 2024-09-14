
from django.urls import path
from . import views

app_name='products'
urlpatterns = [ 
    path("create/",views.create_product_view,name='create'),
]
