# Sample Sales Database Schema

Fictional learning schema; it is not connected to a real company database.

## customers
- customer_id: unique customer identifier (primary key)
- customer_name: customer display name
- region: sales region
- created_at: customer creation timestamp

## orders
- order_id: unique order identifier (primary key)
- customer_id: customer reference to customers.customer_id
- order_date: order date
- order_status: order status
- total_amount: total order value

## order_items
- order_item_id: unique order-line identifier
- order_id: reference to orders.order_id
- product_id: product reference
- quantity: units ordered
- unit_price: price per unit

## products
- product_id: unique product identifier (primary key)
- product_name: product name
- category: product category

## Relationships
- customers.customer_id = orders.customer_id
- orders.order_id = order_items.order_id
- order_items.product_id = products.product_id

## Metric: total revenue by customer
For this sample schema, sum orders.total_amount by customer. Confirm the business definition before excluding order statuses. Avoid joining orders to order_items while summing orders.total_amount unless you aggregate carefully, because the join can duplicate order totals.
