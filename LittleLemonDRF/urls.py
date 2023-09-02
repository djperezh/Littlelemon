from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register("category", views.CategoryViewSet, basename="category")
router.register("menu-items", views.MenuItemViewSet, basename="menu-items")

urlpatterns = [
    path("", include(router.urls)),
    # path("cart", views.CartView.as_view(), name="cart"),
    path("cart/menu-items", views.CartView.as_view(), name="cart"),
    path("cart/menu-items/<int:pk>", views.CartItemView.as_view(), name="cart-detail"),
    path("orders", views.OrdersView.as_view(), name="orders"),
    path("orders/<int:pk>", views.OrderItemView.as_view(), name="orders-detail"),
]