# Littlelemon
Example application in Python using Django Framework

By Coursera:
* [Meta - API](https://www.coursera.org/learn/apis?specialization=meta-back-end-developer)

* [Meta - The Full Stack](https://www.coursera.org/learn/the-full-stack)

# FrontEnd (Booking) Functional requirement

1. Is the app added to the installed apps list in the settings file?

2. Is the database configuration updated inside the settings file?

3. Were migrations performed?

4. Are there three fields in the booking form: First name, Reservation date and Reservation slot?

5. Does a date selector open up when you click on the reservation date field on the booking form?

6. Are all the bookings available as JSON data on the reservations page?

7. Is duplicate booking prohibited on a specific date if the time is already booked?

8. Does changing the date refresh the booking data?

9. Is a duplicate booking on a specific date and time unavailable if the slot is already booked? 

10. Can you display bookings for a specific date using the API?

11. If there is no booking, does a No Booking message show for that date?

12. Was fetch API used to retrieve data from the API?

13. Is the current date automatically selected when you open the booking form?

## Screeshots

![Book & Reservations](/docs/imgs/bookings.png "Book & Reservations")

### [Run locally - Setup](/docs/run-setup.md)

# BackEnd (API) Functional requirement

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

NOTE: See [Rubric](/docs/rubric.md) for more details.

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

### [Run locally - Setup](/docs/run-setup.md)

### [Development - Setup](/docs/dev-setup.md)