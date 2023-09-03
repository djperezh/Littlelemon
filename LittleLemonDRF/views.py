from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import viewsets
from .models import MenuItem, Category, Cart, Order, OrderItem
from .paginations import MenuItemListPagination
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import ( IsAdmin, IsManager, IsDeliveryCrew, IsCustomer, IsCustomerAndOwner, IsDeliveryCrewAndOwner, ReadOnly,)
from datetime import date
from django.contrib.auth.models import User, Group

# {url}/api/category
class CategoryViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ["title"]
    ordering_fields = ["id", "title"]
    search_fields = ["title"]
    
    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [ReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
# {url}/api/menu-items
class MenuItemViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ["title", "price", "featured", "category"]
    ordering_fields = ["id", "title", "price"]
    search_fields = ["title", "category__title"]
    pagination_class = MenuItemListPagination

    # GET
    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [ReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdmin]

        return [permission() for permission in permission_classes]

    # POST
    def partial_update(self, request, *args, **kwargs):
        menuitem = MenuItem.objects.get(pk=self.kwargs["pk"])
        menuitem.featured = not menuitem.featured
        menuitem.save()

        return Response({"message": f"Featured status of {str(menuitem.title)} was changed to {str(menuitem.featured)}"}, status=status.HTTP_200_OK)    
    
# {url}/api/cart/menu-items
class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    # GET
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    # POST
    def post(self, request, *args, **kwargs):
        serialized_item = self.get_serializer(data=request.data, many=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save(user=self.request.user)
        return Response({"message": f"{serialized_item.data['menuitem']} was successfully added to the cart for {request.user.username}"}, status=status.HTTP_201_CREATED)
    
    # DELETE
    def delete(self, request, *args, **kwargs):
        return Response({"message": f"Cart was successfully emptied for {request.user.username}"}, status=status.HTTP_200_OK)
    
# {url}/api/cart/menu-items/{menuitem_id}
class CartItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    # GET
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404"s below
        menuitem = MenuItem.objects.get(pk=self.kwargs["pk"])
        menuitem_id = menuitem.pk
        obj = queryset.get(menuitem=menuitem_id)
        self.check_object_permissions(self.request, obj)
        return obj
       
# {url}/api/orders
class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "date", "delivery_crew"]
    ordering_fields = ["id", "delivery_crew", "total", "date"]
    permission_classes = [IsAuthenticated]

    # GET
    def get_queryset(self):
        if IsManager().has_permission(self.request, self) or IsAdmin().has_permission(
            self.request, self
        ):
            return Order.objects.all()
        elif IsDeliveryCrew().has_permission(self.request, self):
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)

    # POST
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)

        if cart.exists():
            total = 0
            order = Order.objects.create(user=request.user, status=False, total=total, date=date.today)

            for cart_item in cart.values():
                menuitem = get_object_or_404(MenuItem, id=cart_item["menuitem_id"])
                order_item = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=cart_item["quantity"])
                order_item.save()
                total += float(menuitem.price) * cart_item["quantity"]

            order.total = total
            order.save()
            cart.delete()

            return Response({"message": f"Order {order.id} for {request.user.username} was successfully added"}, status=status.HTTP_201_CREATED)

        return Response({"message": f"There is not item in the cart!"}, status=status.HTTP_400_BAD_REQUEST,)
        
# {url}/api/orders/{order_id}
class OrderItemView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderItemSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["menuitem", "order__status", "order__delivery_crew"]
    ordering_fields = ["id", "menuitem", "menuitem__price", "order__status", "order__delivery_crew"]
    search_fields = ["menuitem", "order__status", "order__delivery_crew"]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            permission_classes = [IsManager | IsAdmin]
        elif self.request.method == "PATCH":
            permission_classes = [IsManager | IsAdmin | IsDeliveryCrewAndOwner]
        else:
            permission_classes = [IsManager | IsAdmin | IsDeliveryCrew | IsCustomer]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs["pk"])

    # GET
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serialized_items = self.get_serializer(queryset, many=True)
        order = Order.objects.get(pk=self.kwargs["pk"])
        
        if IsDeliveryCrewAndOwner().has_object_permission(
            self.request, self, order
        ) or IsCustomerAndOwner().has_object_permission(self.request, self, order):
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        elif IsManager().has_permission(self.request, self) or IsAdmin().has_permission(
            self.request, self
        ):
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You do not have permission to see this page!"}, status.HTTP_403_FORBIDDEN)

    # PATCH
    def partial_update(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs["pk"])
        order.status = not order.status
        order.save()

        return Response({"message": f"Status of order # {str(order.id)} was changed to {str(order.status)}"}, status=status.HTTP_200_OK)

    # PUT
    def update(self, request, *args, **kwargs):
        serialized_order = self.get_serializer(data=request.data)
        serialized_order.is_valid(raise_exception=True)
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        crew = get_object_or_404(User, username=request.data["username"])
        order.delivery_crew = crew
        order.save()

        return Response({"message": f"{str(crew.username)} was assigned to order # {str(order.id)}"}, status=status.HTTP_201_CREATED)

    # DELETE
    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs["pk"])
        order_number = str(order.id)
        order.delete()

        return Response({"message": f"Order {order_number} was successfully deleted for {request.user.username}"}, status=status.HTTP_200_OK)


class ManagerPostView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    # POST
    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")

            if (
                user.groups.count() == 0
                and user.is_staff == False
                and user.is_active == True
            ):
                # add status = Staff and save changes
                user.is_staff = True
                user.save()

            managers.user_set.add(user)

            return Response({"message": f"{username} was successfully added to 'Manager' group"}, status=status.HTTP_201_CREATED)

        return Response({"message": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

class ManagerDeleteView(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    # DELETE
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        if user.groups.count() == 0 and user.is_staff == True:
            # remove status = Staff and save changes
            user.is_staff = False
            user.save()

        return Response({"message": f"{user.username} successfully removed from 'Manager' group"}, status=status.HTTP_200_OK)
    
class DeliveryCrewPostView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Delivery Crew")
    serializer_class = UserSerializer
    permission_classes = [IsManager | IsAdmin]

    # POST
    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crews = Group.objects.get(name="Delivery Crew")

            if (
                user.groups.count() == 0
                and user.is_staff == False
                and user.is_active == True
            ):
                # add status = Staff and save changes
                user.is_staff = True
                user.save()

            delivery_crews.user_set.add(user)

            return Response({"message": f"{username} was successfully added to 'Delivery Crew' group"}, status=status.HTTP_201_CREATED)

        return Response({"message": "username field is required"}, status=status.HTTP_400_BAD_REQUEST)
    
class DeliveryCrewDeleteView(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Delivery Crew")
    serializer_class = UserSerializer
    permission_classes = [IsManager | IsAdmin]

    # DELETE
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        delivery_crews = Group.objects.get(name="Delivery Crew")
        delivery_crews.user_set.remove(user)
        if user.groups.count() == 0 and user.is_staff == True:
            # remove status = Staff and save changes
            user.is_staff = False
            user.save()

        return Response({"message": f"{user.username} was successfully removed from 'Delivery Crew' group"}, status=status.HTTP_200_OK)