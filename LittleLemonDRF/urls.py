from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
]