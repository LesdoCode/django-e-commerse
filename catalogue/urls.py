from django.urls import path, include
from .views import (
    HomeView, 
    ProductDetail,
    add_to_cart,
    remove_from_cart,
    OrderSummary,
    remove_single_from_cart,
    CheckOutView,
    delivery,
    item_search,
    proof_of_pay,
    order_success,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>', ProductDetail.as_view(), name='product'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_from_cart/<slug>/', remove_single_from_cart, name='remove_single_from_cart'),
    path('order-summary/', OrderSummary.as_view(), name='order_summary'),
    path('accounts/profile/', HomeView.as_view(), name='home'),
    path('delivery/', delivery, name='delivery'),
    path('item_search', item_search, name='item_search'),
    path('proof_of_pay', proof_of_pay, name='proof_of_pay'),
    path('order_success', order_success, name='order_success'),
]
