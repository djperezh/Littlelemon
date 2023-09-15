# Littlelemon - Restaurant

> Example application in Python using Django Framework

<P>&nbsp;</P>

<img alt="Climate" src="https://img.shields.io/badge/SetUp-Environment-3178C6?logoColor=white&style=for-the-badge" />

* [Run locally - Setup](/docs/run-setup.md)
* [Development - Setup](/docs/dev-setup.md)

<P>&nbsp;</P>

<img alt="Climate" src="https://img.shields.io/badge/Functional requirement-Rubric-3178C6?logoColor=white&style=for-the-badge" />

<details>
  <summary>FrontEnd</summary>

```
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
```

### Screeshots

![Book & Reservations](/docs/imgs/bookings.png "Book & Reservations")

</details>

<details>
  <summary>BackEnd</summary>

```
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
```

> NOTE: See [Rubric](/docs/rubric.md) for more details.

</details>

<details>
  <summary>Capstone project</summary>

```
    1. Does the web application use Django to serve static HTML content?

    2. Has the learner committed the project to a Git repository?

    3. Does the application connect the backend to a MySQL database?

    4. Are the menu and table booking APIs implemented?

    5. Is the application set up with user registration and authentication?

    6. Does the application contain unit tests?

    7. Can the API be tested with the Insomnia REST client?
```
</details>

<P>&nbsp;</P>
<img alt="Climate" src="https://img.shields.io/badge/Endpoints-API-3178C6?logoColor=white&style=for-the-badge" />

> _url = "http://127.0.0.1:8000/" for local environment_

<details>
  <summary>FrontEnd</summary>

```
{url}/restaurant/           [name='home']
{url}/restaurant/about      [name='about']
{url}/restaurant/book       [name='book']
{url}/restaurant/bookings   [name='bookings']
```

</details>

<details>
  <summary>BackEnd API</summary>

> Use Browser or Insomia/Postmand to call API's (use {url}/auth/token/login Endpoint to get Token)

```
{url}/restaurant/booking/tables                         [name='tables']
{url}/restaurant/menu/                                  [name='menu']
{url}/restaurant/menu/{menuitem_id}                     [name='menu']
{url}/restaurant/api/menu-items                         [name='menu-items-list']
{url}/restaurant/api/menu-items/{menuitem_id}           [name='menuitem-detail']
{url}/restaurant/api/categories                         [name='categories-list']
{url}/restaurant/api/categories/{category_id}           [name='category-detail']
{url}/restaurant/cart/menu-items                        [name='cart']
{url}/restaurant/cart/menu-items/{cartitem_id}          [name='cartitem-detail']
{url}/restaurant/cart/orders                            [name='orders']
{url}/restaurant/cart/orders/{oredr_id}                 [name='orders-detail']
{url}/restaurant/groups/manager/users                   [name='manager']
{url}/restaurant/groups/manager/users/{user_id}         [name='manager-detail']
{url}/restaurant/groups/delivery-crew/users             [name='delivery-crew']
{url}/restaurant/groups/delivery-crew/users/{user_id}   [name='delivery-crew-detail']
```

![Order Endpoints](/docs/imgs/order.png "Order Enpoints")

![Cart Endpoints](/docs/imgs/cart.png "Cart Endpoints")

![Users Endpoints](/docs/imgs/users.png "Users Endpoints")

</details>

<details>
  <summary>Dosier generated</summary>

```
{url}/admin/
{url}/auth/
{url}/auth/
```

![Djoser Endpoints](/docs/imgs/djoser.png "Djoser Endpoints")

</details>

<details>
  <summary>Error Handling</summary>

> This enpoins should handle errors by returning the corresponding HTTP status code

![HTTP status code](/docs/imgs/errors.png "HTTP status code")

</details>

<P>&nbsp;</P>

<img alt="Climate" src="https://img.shields.io/badge/META BackEnd Developer -Specialization By Coursera-3178C6?logoColor=white&style=for-the-badge" />

* [Meta - API](https://www.coursera.org/learn/apis?specialization=meta-back-end-developer)
* [Meta - The Full Stack](https://www.coursera.org/learn/the-full-stack)
* [Meta - BackEnd Developer Capstone](https://www.coursera.org/learn/back-end-developer-capstone)

<P>&nbsp;</P>

> THIS PROJECT IS FOR LEARNING PURPOSES ONLY AND STRICTLY FOR PERSONAL AND PRIVATE USE. YOU CAN USE IT AS REFERENCE ONLY SINCE THIS IS **NOT** `PRODUCTION` QUALITY CODE