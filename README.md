 Dynamic Pricing and Inventory Management System  

## Introduction  
In today’s competitive market, businesses need to adjust product prices and manage inventory efficiently to maximize profits and customer satisfaction. This project combines **Q-Learning** (a reinforcement learning algorithm) and **Random Forest regression** to create a smart system that dynamically adjusts product prices based on demand and inventory levels.  

## Purpose  
The goal of this project is to build a smart pricing and inventory management system that:  
- **Predicts optimal product prices** using Random Forest regression.  
- **Adjusts prices dynamically** with Q-Learning to maximize profit.  
- **Optimizes inventory levels** to avoid overstocking or stockouts.  
- **Provides insights** for administrators to improve pricing and inventory strategies.  
- **Enhances customer satisfaction** through adaptive pricing and better product availability.  

## Problem Context  
Businesses often struggle with:  
- Overpricing or underpricing products.  
- Overstocking or running out of stock due to poor demand prediction.  
- Lack of visibility into how sales, inventory, and customer feedback are connected.  

## Solution Overview  
### 1. **Random Forest Regression**  
- Predicts initial product prices based on key factors like cost, sales trends, and stock levels.  

### 2. **Q-Learning for Dynamic Pricing**  
- Identifies demand states (high, medium, low, no demand).  
- Recommends price adjustments (increase, decrease, or maintain).  
- Uses a reward system to maximize profit and balance inventory.  

### 3. **System Features**  
- **User Module** – Customers can purchase products, give feedback, and view updated ratings.  
- **Admin Module** – Admins can update prices, add new products, and manage inventory.  
- **Integrated Machine Learning** – Combines Random Forest and Q-Learning for dynamic optimization.  

## Dataset Description  
The dataset includes key information to drive pricing and inventory decisions:  
- **Product ID** – Unique identifier for each product.  
- **Cost Price** – Product’s production or purchase cost.  
- **Stock Level** – Current product availability in inventory.  
- **Current Sales** – Number of units sold recently.  
- **Total Sales** – Total number of units sold over time.  
- **Customer Rating** – Average customer rating (1–5).  
- **Competitor Price** – Price set by competitors.  
- **Max Price** – Maximum allowed selling price.  
- **Initial Price** – Starting selling price based on cost and margin.

- SCREENSHOTS:
- 
![pic1p1](https://github.com/user-attachments/assets/cf3bd5ac-05d2-4562-838d-1e54569bd929)
![pic4p1](https://github.com/user-attachments/assets/95454183-f774-4279-a964-348ed4f9cf12)
![pic2p1](https://github.com/user-attachments/assets/1723fa3e-cc0a-41e2-b12f-38b6f4c5ebb9)
![pic3p1](https://github.com/user-attachments/assets/158177e9-2b73-4b55-aa72-e28fcf82ccae)



