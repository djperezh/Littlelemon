from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import viewsets
from .models import MenuItem, Category, Cart, Order, OrderItem
from .paginations import MenuItemListPagination
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CategoryViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class MenuItemViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "inventory"]
    filterset_fields = ["price", "inventory"]
    search_fields = ["title"]
    pagination_class = MenuItemListPagination

# {url}/api/cart/menu-items
class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]
    
    # GET
    def get_queryset(self):
        return Cart.objects.all()
    
    # POST
    def post(self, request, *args, **kwargs):
        return Response({"message": "TODO: POST"}, status=status.HTTP_201_CREATED)

    # DELETE
    def delete(self, request, *args, **kwargs):
        return Response({"message": "TODO: DELETE"}, status=status.HTTP_200_OK)
    
# {url}/api/cart/menu-items/{menuitem_id}
class CartItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.all()
        # return Cart.objects.filter(user=self.request.user)
    
    # GET
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            # make sure to catch 404"s below
            menuitem = MenuItem.objects.get(pk=self.kwargs["pk"])
            menuitem_id = menuitem.pk
            
            obj = queryset.get(menuitem=menuitem_id)
            # self.check_object_permissions(self.request, obj)
            return obj
        
        return Response({"message": "TODO: GET >> There is Items in cart!"}, status=status.HTTP_400_BAD_REQUEST)
        
# {url}/api/orders
class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "date", "delivery_crew"]
    ordering_fields = ["id", "delivery_crew", "total", "date"]
    # permission_classes = [IsAuthenticated]

    # GET
    def get_queryset(self):
        return Order.objects.all()

    # POST
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.all()

        if cart.exists():
            return Response({"message": "TODO: POST"}, status=status.HTTP_201_CREATED)

        # No items in the cart
        return Response({"message": "TODO: POST >> There is not item in the cart!"}, status=status.HTTP_400_BAD_REQUEST)
    
# {url}/api/orders/{order_id}
class OrderItemView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderItemSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["menuitem", "order__status", "order__delivery_crew"]
    ordering_fields = ["id", "menuitem", "menuitem__price", "order__status", "order__delivery_crew"]
    search_fields = ["menuitem", "order__status", "order__delivery_crew"]

    # def get_permissions(self):
    #     if self.request.method in ["PUT", "DELETE"]:
    #         permission_classes = [IsManager | IsAdmin]
    #     elif self.request.method == "PATCH":
    #         permission_classes = [IsManager | IsAdmin | IsDeliveryCrewAndOwner]
    #     else:
    #         permission_classes = [IsManager | IsAdmin | IsDeliveryCrew | IsCustomer]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs["pk"])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            serialized_items = self.get_serializer(queryset, many=True)
            order = Order.objects.get(pk=self.kwargs["pk"])
        
            return Response({"message": "TODO: GET"}, status=status.HTTP_201_CREATED)

        # No items in the cart
        return Response({"message": "TODO: GET >> No elements"}, status=status.HTTP_400_BAD_REQUEST)
    


        # if IsDeliveryCrewAndOwner().has_object_permission(
        #     self.request, self, order
        # ) or IsCustomerAndOwner().has_object_permission(self.request, self, order):
        #     return Response(serialized_items.data, status=status.HTTP_200_OK)
        # elif IsManager().has_permission(self.request, self) or IsAdmin().has_permission(
        #     self.request, self
        # ):
        #     return Response(serialized_items.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(
        #         {"message": "You do not have permission to see this page!"},
        #         status.HTTP_403_FORBIDDEN,
        #     )

        return Response(serialized_items.data, status=status.HTTP_200_OK)
    
    # PATCH
    def partial_update(self, request, *args, **kwargs):
        # order = Order.objects.get(pk=self.kwargs["pk"])
        # order.status = not order.status
        # order.save()

        return Response({"message": "TODO: PATCH"}, status=status.HTTP_200_OK)

    # PUT
    def update(self, request, *args, **kwargs):
        # serialized_order = self.get_serializer(data=request.data)
        # serialized_order.is_valid(raise_exception=True)
        # order = get_object_or_404(Order, pk=self.kwargs["pk"])
        # crew = get_object_or_404(User, username=request.data["username"])
        # order.delivery_crew = crew
        # order.save()

        return Response({"message": "TODO: PUT"}, status=status.HTTP_201_CREATED)

    # DELETE
    def delete(self, request, *args, **kwargs):
        # order = Order.objects.get(pk=self.kwargs["pk"])
        # order_number = str(order.id)
        # order.delete()

        return Response({"message": "TODO: DELETE"}, status=status.HTTP_200_OK)
