from datetime import date
from django.contrib.auth.models import User, Group
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse
from rest_framework import generics, status
# from rest_framework.decorators import api_view, renderer_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .forms import BookingForm, ReservationsForm
from .models import MenuItem, Category, Cart, Order, OrderItem, Menu, Booking
from .paginations import MenuItemListPagination
from .permissions import ( IsAdmin, IsManager, IsDeliveryCrew, IsCustomer, IsCustomerAndOwner, IsDeliveryCrewAndOwner, ReadOnly)
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer, BookingSerializer

import json

# Navigation (Static pages)
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

# {url}/restaurant/book
def book(request):
    form = BookingForm()
    date_filter = str(date.today())
    flag = False
    
    # POST
    if request.method == 'POST':
        form = BookingForm(request.POST)
        date_filter = request.POST.get('date', None)
        if form.is_valid():
            form.save()            
            date_filter = request.POST.get('date', None)

    # GET
    if request.method == "GET":
        if request.GET.get('date', None):
            date_filter = request.GET.get('date', None)
        
    reservations = Booking.objects.filter(date=date_filter)
    if reservations.count() > 0:
        flag = True
        
    context = {'form': form, 'reservations': reservations, 'date_filter': date_filter, 'flag':flag}

    return render(request, 'book.html', context)

# {url}/restaurant/bookings (Reservations list using JSON)
def bookings(request):
    # GET
    content = Booking.objects.all()
    
    if request.method == "GET":
        if request.GET.get('date', None):
            content = Booking.objects.filter(date=request.GET.get('date', None))
        else:
            content = Booking.objects.all()
            
    reservations = json.loads(serialize("json", content))        
    json_pretty = json.dumps(reservations, indent=4)
    context = {"reservations": json_pretty}
    return render(request, "reservations.html", context)

# {url}/restaurant/api/tables (Django generated)
class BookingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    # GET
    def get_queryset(self):
        return Booking.objects.all()

    # POST
    def create(self, request): # Here is the new update comes <<<<
        booking = Booking.objects.create(name=request.POST.get('name'), guests=request.POST.get('guests'), date=request.POST.get('date'), time=request.POST.get('time'))
        booking.save()
        
        # do something with post data
        return Response({"message": f"{str(booking.name)} was booked"}, status=status.HTTP_201_CREATED)
    
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

# {url}/restaurant/menu
class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuItemSerializer
    
    # GET
    def get_queryset(self):
        return MenuItem.objects.all()

# {url}/restaurant/menu/{menuitem_id}
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        menuitem = MenuItem.objects.get(pk=self.kwargs["pk"])
        menuitem_id = menuitem.pk
        obj = queryset.get(id=menuitem_id)
        # self.check_object_permissions(self.request, obj)
        return obj

def display_menu_item(request, pk=None):
    if pk:
        menu_item = MenuItem.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, 'menu_item.html', {"menu_item": menu_item})

# {url}/restaurant/api/categories (Django generated)
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
    
# {url}/restaurant/api/menu-items (Django generated)
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
    
# {url}/restaurant/cart/menu-items
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
        return Response({"message": f"Item was successfully added to the cart for {request.user.username}"}, status=status.HTTP_201_CREATED)
    
    # DELETE
    def delete(self, request, *args, **kwargs):
        return Response({"message": f"Cart was successfully emptied for {request.user.username}"}, status=status.HTTP_200_OK)
    
# {url}/restaurant/cart/menu-items/{menuitem_id}
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
        date = request.data["date"]

        if cart.exists():
            total = 0
            order = Order.objects.create(user=request.user, status=False, total=total, date=date)

            for cart_item in cart.values():
                menuitem = get_object_or_404(MenuItem, id=cart_item["menuitem_id"])
                order_item = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=cart_item["quantity"])
                order_item.save()
                total += float(menuitem.price) * float(cart_item["quantity"])

            order.total = total
            order.save()
            cart.delete()

            return Response({"message": f"Order {order.id} for {request.user.username} was successfully added"}, status=status.HTTP_201_CREATED)

        return Response({"message": f"There is not item in the cart!"}, status=status.HTTP_400_BAD_REQUEST,)
        
# {url}/api/orders/{order_id}
class OrderItemView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderItemSerializer
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
    permission_classes = [IsManager] # [IsAdmin]

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
    queryset = User.objects.filter(groups__name="DeliveryCrew")
    serializer_class = UserSerializer
    permission_classes = [IsManager | IsAdmin]

    # POST
    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crews = Group.objects.get(name="DeliveryCrew")

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
    queryset = User.objects.filter(groups__name="DeliveryCrew")
    serializer_class = UserSerializer
    permission_classes = [IsManager | IsAdmin]

    # DELETE
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        delivery_crews = Group.objects.get(name="DeliveryCrew")
        delivery_crews.user_set.remove(user)
        if user.groups.count() == 0 and user.is_staff == True and user.is_superuser == False:
            # remove status = Staff and save changes
            user.is_staff = False
            user.save()

        return Response({"message": f"{user.username} was successfully removed from 'Delivery Crew' group"}, status=status.HTTP_200_OK)