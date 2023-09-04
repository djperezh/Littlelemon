from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255, blank=None, null=None)

    def __str__(self):
        return self.title
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True, blank=None, null=None)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True, blank=None, null=None)
    inventory = models.SmallIntegerField()
    featured = models.BooleanField(db_index=True, blank=None, null=None)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=None, null=None)
    
    def __str__(self):
        return str(self.title) + " (" + str(self.category) + ")"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, blank=None, null=None)
    quantity = models.DecimalField(max_digits=3, decimal_places=2, blank=None, null=None) # models.IntegerField(blank=None, null=None),
    # unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    # price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('menuitem', 'user')
        
    def __str__(self):
        return self.user
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=0, blank=None, null=None)
    total = models.DecimalField(max_digits=6, decimal_places=2, blank=None, null=None)
    date = models.DateField(db_index=True, auto_now_add=True, blank=None, null=None)
    
    def __str__(self):
        return str(self.user) + " (Order# " + str(self.id) + ")"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, blank=None, null=None)
    quantity = models.DecimalField(max_digits=3, decimal_places=2, blank=None, null=None) # models.SmallIntegerField(blank=None, null=None),
    # unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    # price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menuitem')
    
    def __str__(self):
        return str(self.order) + " - " + str(self.menuitem)