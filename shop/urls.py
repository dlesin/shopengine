# from django.conf.urls import url
# from .views import *


# urlpatterns = [
#     url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
#     url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
#     url(r'^$', base_view, name='base'),
# ]

from django.urls import path
from .views import *


urlpatterns = [
    path('', base_view, name='base_view_url'),
    path('cart/', cart_view, name='cart_view_url'),
    path('category/<str:category_slug>/', category_view, name='category_detail_url'),
    path('product/<str:product_slug>/', product_view, name='product_detail_url'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart_url'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart_url'),
    path('change_item_qty/', change_item_qty, name='change_item_qty_url'),
    path('checkout/', checkout_view, name='checkout_view_url'),
    path('order/', order_create_view, name='order_create_view_url'),
    path('make_order/', make_order_view, name='make_order_view_url'),
    path('thanks/', thanks_view, name='thanks_view_url'),
]
