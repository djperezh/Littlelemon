from django.test import TestCase
from restaurant.models import MenuItem, Category

class MenuItemTest(TestCase):
    def test_create_menuitem(self):
        # Arrange
        expected_menuitem_title = "Menu Item Test"
        expected_category_title = "Category Test"

        # Act
        category_obj = Category.objects.create(title=expected_category_title)
        menuitem_obj = MenuItem.objects.create(title = expected_menuitem_title,price = 1.23,inventory = "123",featured = False,category_id = category_obj.id)
        
        # Assert
        self.assertEqual(menuitem_obj.title, expected_menuitem_title)

class CategoryTest(TestCase):
    def test_create_category(self):
        # Arrange
        expected_category_title = "Category Test"
        
        # Act
        category_obj = Category.objects.create(title=expected_category_title)
        
        # Assert
        self.assertEqual(category_obj.title, expected_category_title)