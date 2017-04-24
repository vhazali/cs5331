# Assignment 1 - Opencart

## Accessing the webpage

#### VM's IP Address
 - This can be done by configuring the host-only adapter settings for virtualbox.
 - However, for the opencart to work properly, the `config.php` files at `opencart/admin/config.php` and `opencart/config.php` must be edited. The `HTTP_SERVER` and `HTTPS_SERVER` variables defined in there must be changed.
 - The `localhost` in these variables should be replaced with the assigned IP address of the VMs. As this is dependent on the testing environment, I have decided to leave it as localhost.

### Localhost
 - This can be done by configuring the NAT adapter settings for virtualbox.
 - Port-forward TCP port 80 from the guest to the host's TCP port 80, and opencart should work fine.

## Easy (You might also like)
Function is implemented at the bottom of the product page, below the description frame.

####How this function works:
 - Look at the current product (A), and get all the categories that it belongs to
 - For each of the category, look up the most popular product
 - Display the most popular product for all the categories
 - Updates for suggestion
  - The Cameras section has purposely not been bought. This is to make it easier to demonstrate that the suggestion will update correctly.
  - Simply buy any of the two camera, and go back to viewing the cameras. 
  - Of course, this functionality correctly works for other categories! (Just that you might need to buy a lot more items ;) )

####Gotchas:
 - Does not show the same product B, if product A and B has more than one common category and B is the most popular product in both.
 - Does not show any product if A is already the most popular product in its category.
 - In the event that there is no "most popular product", the "You might also like" section is hidden altogether
 - In the event that there is more than one most popular product, the SQL query will still only return one.
 - Most popular product is defined as the product with the most number of orders placed for.
  - This does not make any assertion on the order status. Simply counts the number of orders this product shows up in.
  - **Even if an order was cancelled, refunded, etc. it will still count to the product's popularity**

## Advanced
 
### Customer-specific Sale Statistics
 - Implemented under `Reports->Sales->Customer` tab on the home page ribbon.
 - To view any specific customer, simply click on the customer's name.
 - Other pages that also allows for clicking on customer's name:
  1. Dashboard
  2. Sales->Orders

### Referrer ID
 - Implemented the input in the checkout page to reduce the number of times user need to enter referrer's ID
 - Attaches referral ID to all order records (in database, the `oc_order` table)
 
### Best Referrer and Best Customer
 - Best referrer is defined as the customer that has been attributed the most number of times as a referrer (in the checkout page)
 - Best Customer is defined as the customer that has made the most number of orders
  - This again does not make any assertion on the order statuses.
  - **Even if an order was cancelled, refunded, etc. it will still count positively to the customer
  
### Export to CSV
 - Implemented in exactly 3 places:
  1. `Reports->Sales->Order`
  2. `Reports->Sales->Shipping`
  3. `Reports->Products->Viewed`
  
## Undone
 - Day, week and yearly view
