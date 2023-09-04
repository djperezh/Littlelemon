# Functional Test

* Test if the admin can assign users to the manager group:
Make a POST call to this endpoint http://127.0.0.1:8000/api/groups/manager/users with a valid admin toke and a valid username in the HTTP REQUEST body. 

        Was the user added to the manager group with an admin token?

* Test if you can access the manager group with an admin token:
Make a GET call to http://127.0.0.1:8000/api/groups/manager/users with an admin token. 

        Is there a list of users from the manager group in the API output?

* Test if the admin can add menu items:
Make a POST call to this endpoint http://127.0.0.1:8000/api/menu-items with the admin token and necessary data. Or, log into the Django admin panel as super admin and then browse this endpoint in your browser and add some menu items. 

        Can the admin add menu items? 

* Test if the admin can add categories:
Make a POST call to this endpoint http://127.0.0.1:8000/api/categories with the admin token and necessary data. Or log into the Django admin panel as super admin and then browse this endpoint in your browser and add some menu items.

        Can the admin add categories? 

* Test if the manager can log in:
Make a POST call to this endpoint  http://127.0.0.1:8000/auth/token/login/ with the username and password of a manager.

        Is the access token in the API output? 
* Test if the manager can update the item of the day:
Make a PATCH call to the endpoint of any single menu item endpoint like this http://127.0.0.1:8000/api/menu-items/1 Opens in a new tab with a manager token. Add a featured field in the REQUEST body with its value set to true or false. 

        Did the value of the featured field update for this particular menu item?

* Test if the manager can assign users to the delivery crew:
Make a POST call to this endpoint http://127.0.0.1:8000/api/groups/manager/users Opens in a new tab with a valid manager token and a valid username in the HTTP REQUEST body. 

        Can the manager assign users to the delivery crew group? 

* Test if the manager can assign orders to the delivery crew:
Make a PATCH call to an endpoint of any single order item like this http://127.0.0.1:8000/api/orders/1 Opens in a new tab with a manager token. Add a delivery_crew field in the REQUEST body with its value set to any delivery crew user id.

        Can the managers assign orders to a delivery crew? 

* Test if the delivery crew can view orders assigned to them:
Make a GET call to this endpoint http://127.0.0.1:8000/api/orders Opens in a new tab with a delivery crew token.

        Can the delivery crew browse orders that were assigned to them? 

* Test if the delivery crew can update an order as delivered:
Make a PATCH call to this endpoint to any single order item endpoint like this http://127.0.0.1:8000/api/orders/1 Opens in a new tab with a delivery crew token. Add a status field in the REQUEST body with its value set to true or false.

        Can the delivery crew update the order status? 

* Test if customers can register:
Make a POST call to this endpoint http://127.0.0.1:8000/auth/users/ with a username, password and email in the HTTP REQUEST body.

        Can customers register using this endpoint?

* Test if customers can log in using their username and password and get access tokens:
Make a POST call to this endpoint http://127.0.0.1:8000/auth/token/login/ with a valid username and password in the HTTP Request body. 

        Is the access token visible in the API output? 

* Test if customers can browse all categories:
Make a GET API call to this endpoint http://127.0.0.1/api/categories with a customer token

        Are the categories visible to customers? 

* Test if customers can browse all menu items:
Make a GET API call to this endpoint http://127.0.0.1/api/menu-items with a customer token

        Are the menu items visible to customers? 

* Test if customers can browse menu items by category:
Make a GET API call to these endpoints, http://127.0.0.1:8000/api/menu-items?search=Icecream or any available category name instead of Icecream with a customer token.

        Do the menu items in the category display for customers?

* Test if customers can paginate menu items:
Make a GET API call to the endpoints http://127.0.0.1:8000/api/menu-items?page=1 or http://127.0.0.1:8000/api/menu-items?page=2 with a customer token.

        
        Do the menu items display proper pagination for customers? 

* Test if customers can sort menu items by price:
Make a GET API call to the endpoint http://127.0.0.1:8000/api/menu-items?ordering=price or http://127.0.0.1:8000/api/menu-items?ordering=-price with a customer token.

        Are the menu items properly sorted by price in ascending or descending order for customers?
 
* Test if customers can add menu items to the cart:
Make a POST call to this endpoint http://127.0.0.1:8000/api/cart/menu-items with a customer token. Add these fields with valid data in the REQUEST body for menuitem, unit_price, quantity.

        
        Can customers add menu items to the cart? 

* Test if customers can see previously added items in the cart:
Make a GET call to this endpoint http://127.0.0.1:8000/api/cart/menu-items with a customer token. 

        Are previous items added to the cart visible for customers? 

* Test if customers can place orders:
Make a POST call to this endpoint http://127.0.0.1:8000/api/cart/orders with a customer token. Add only the date field with valid data in the REQUEST body. Here is a sample date – 2022-11-16.

        Can customers successfully place an order? 

* Customers can view their own orders:
Make a GET call to this endpoint http://127.0.0.1:8000/api/cart/orders with a customer token. 

        Can customers browse their own orders? 
