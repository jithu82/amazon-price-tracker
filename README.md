
# E-Commerce Price Tracker

A Python-based price monitoring system that tracks product prices, stores price history in SQLite, organizes products into categories, and sends email alerts when prices fall below user-defined thresholds.

## Features

### Product Management

- Add products
- Remove products
- Store product URLs
- Organize products into categories

### Category Management

- Create categories
- Add products to categories
- Track category-wise pricing

### Price Tracking

- Fetch price of a single product
- Fetch prices of all products in a category
- Fetch prices of all tracked products

### Notifications

- Set price thresholds
- Automatic email alerts
- Notification when price drops below threshold

### Data Storage

- SQLite database storage
- Historical price tracking
- Product management records

## Product Information

Each product contains:

- Product Name
- Product URL
- Current Price
- Threshold Price

## Available Operations

### Add Product

Stores:

- Product name
- Product URL

### Add Category

Creates a new category for organizing products.

### Add Product To Category

Associates products with specific categories.

### Set Threshold

Defines the target price for notifications.

### Fetch Price Of Single Product

Checks and updates the price of one product.

### Fetch Price Of Category

Checks and updates prices for all products in a category.

### Fetch Price Of All Products

Checks and updates every tracked product.

## Alert System
When:
Current Price <= Threshold Price
