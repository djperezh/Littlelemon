from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("menu-items", views.MenuItemViewSet, basename="menu-items")

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("book", views.book, name="book"),
    path("bookings", views.bookings, name="bookings"),
    # path("menu", views.menu, name="menu"),
    path('menu/', views.MenuItemsView.as_view(), name="menu"),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view(), name="menu"),
    
    path("api/", include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path("cart/menu-items", views.CartView.as_view(), name="cart"),
    path("cart/menu-items/<int:pk>", views.CartItemView.as_view(), name="cart-detail"),
    path("cart/orders", views.OrdersView.as_view(), name="orders"),
    path("cart/orders/<int:pk>", views.OrderItemView.as_view(), name="orders-detail"),
    path("groups/manager/users", views.ManagerPostView.as_view(), name="manager"),
    path("groups/manager/users/<int:pk>", views.ManagerDeleteView.as_view(), name="manager-detail"),
    path("groups/delivery-crew/users", views.DeliveryCrewPostView.as_view(),name="delivery-crew"),
    path("groups/delivery-crew/users/<int:pk>", views.DeliveryCrewDeleteView.as_view(), name="delivery-crew-detail"),
]