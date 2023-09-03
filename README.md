# Littlelemon
Example application in Python using Django Framework

By Coursera: [Meta API](https://www.coursera.org/learn/apis?specialization=meta-back-end-developer)

# Functional requirement

1. The admin can assign users to the manager group

2.	You can access the manager group with an admin token

3.	The admin can add menu items 

4.	The admin can add categories

5.	Managers can log in 

6.	Managers can update the item of the day

7.	Managers can assign users to the delivery crew

8.	Managers can assign orders to the delivery crew

9.	The delivery crew can access orders assigned to them

10. The delivery crew can update an order as delivered

11. Customers can register

12.	Customers can log in using their username and password and get access tokens

13.	Customers can browse all categories 

14.	Customers can browse all the menu items at once

15.	Customers can browse menu items by category

16.	Customers can paginate menu items

17.	Customers can sort menu items by price

18.	Customers can add menu items to the cart

19.	Customers can access previously added items in the cart

20.	Customers can place orders

21.	Customers can browse their own orders

## Endpoints

![Menu Items Endpoints](/docs/imgs/menu-items.png "Menu Items Endpoints")

![order Endpoints](/docs/imgs/order.png "Order Enpoints")

![Cart Endpoints](/docs/imgs/cart.png "Cart Endpoints")

![Users Endpoints](/docs/imgs/users.png "Users Endpoints")

* NOTE: Use djoiser for creating these Endpoints
![Djosier Endpoints](/docs/imgs/djosier.png "Djosier Endpoints")


![Groups Endpoints](/docs/imgs/groups.png "Groups Endpoints")

* This enpoins should handle errors by returning the corresponding HTTP status code
![HTTP status code](/docs/imgs/errors.png "HTTP status code")

# [Run locally - Setup](/docs/run-setup.md)

# [Development - Setup](/docs/dev-setup.md)