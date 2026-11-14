# TARGET APPLICATIONS & EXACT DOM SELECTORS

## 1. UI Target: https://www.saucedemo.com
- Credentials:
  - Valid User: `standard_user`
  - Locked User: `locked_out_user`
  - Password for all: `secret_sauce`
- Login Page Selectors:
  - Username input: `[data-test="username"]`
  - Password input: `[data-test="password"]`
  - Login button: `[data-test="login-button"]`
  - Error message banner: `[data-test="error"]`
- Inventory Page Selectors:
  - Inventory container: `[data-test="inventory-container"]`
  - Add Backpack to cart: `[data-test="add-to-cart-sauce-labs-backpack"]`
  - Add Bike Light to cart: `[data-test="add-to-cart-sauce-labs-bike-light"]`
  - Shopping cart badge: `[data-test="shopping-cart-badge"]`
  - Shopping cart link: `[data-test="shopping-cart-link"]`
- Cart & Checkout Selectors:
  - Checkout button: `[data-test="checkout"]`
  - First Name input: `[data-test="firstName"]`
  - Last Name input: `[data-test="lastName"]`
  - Postal Code input: `[data-test="postalCode"]`
  - Continue button: `[data-test="continue"]`
  - Subtotal label: `[data-test="subtotal-label"]`
  - Tax label: `[data-test="tax-label"]`
  - Total label: `[data-test="total-label"]`
  - Finish button: `[data-test="finish"]`
  - Complete header: `[data-test="complete-header"]` (Expected text: "Thank you for your order!")

## 2. API Target: https://restful-booker.herokuapp.com
- POST `/auth`: Body `{"username": "admin", "password": "password123"}` -> Returns `{"token": "..."}`
- POST `/booking`: Creates a booking -> Returns `{"bookingid": 123, "booking": {...}}`
- GET `/booking/{id}`: Returns booking JSON object
- PUT `/booking/{id}`: Requires header `Cookie: token=<token>` and `Accept: application/json`
- DELETE `/booking/{id}`: Requires header `Cookie: token=<token>` -> Returns HTTP 201