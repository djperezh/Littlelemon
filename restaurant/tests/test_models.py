from django.test import TestCase
from restaurant.models import MenuItem, Category

class MenuItemTest(TestCase):
    def test_get_item(self):
        # category = Category.objects.get(pk=3)
        item = MenuItem.objects.create(
                title = "IceCream",
                price = 3,
                inventory = "3",
                featured = False,
                category_id = 2
        )
        itemstr = item.get_item()
        
        self.assertEqual(itemstr, "IceCream : 3")
        
