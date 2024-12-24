import pandas as pd
import os
import shutil
import numpy as np
import random
from sklearn.ensemble import RandomForestRegressor

DATA_FILE = "C:\\Users\\saisa\\OneDrive\\Desktop\\product_data.csv"

# Q-Learning Parameters
states = ['high_demand', 'medium_demand', 'low_demand', 'no_demand']
actions = ['increase_20', 'increase_10', 'decrease_10', 'decrease_20', 'maintain']
state_to_index = {state: i for i, state in enumerate(states)}
action_to_index = {action: i for i, action in enumerate(actions)}
q_table = np.zeros((len(states), len(actions)))  # Initialize Q-table
learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 0.2


def load_data(file_path):
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        print(f"Error: File '{file_path}' does not exist.")
        exit()
    return data


def save_data(data, file_path):
    try:
        temp_file = file_path + ".tmp"
        data.to_csv(temp_file, index=False) 
        shutil.move(temp_file, file_path)  
        print("Data saved successfully!")
    except PermissionError as e:
        print(f"Permission error: {e}. Please close the file if it's open and check permissions.")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# Train and apply Random Forest Model for all products
def random_forest_predict_all(data):
    features = ['Cost Price', 'Stock Level', 'Total Sales']
    target = 'Initial Price'
    data_clean = data.dropna(subset=features + [target])
    X = data_clean[features]
    y = data_clean[target]
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    data['Predicted Price'] = model.predict(data[features])
    data['Initial Price'] = data['Predicted Price'].round(2)
    print("Random Forest applied to all products, and Initial Prices updated.")
    
  
    save_data(data, DATA_FILE)

def user_login():
    print("\n--- User Login ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    users = {'user1': 'password1', 'user2': 'password2'}
    if username in users and users[username] == password:
        print(f"Welcome {username}!")
        return username
    else:
        print("Invalid username or password.")
        return None

def admin_login():
    print("\n--- Admin Login ---")
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    admins = {'admin1': 'adminpass1', 'admin2': 'adminpass2'}
    if username in admins and admins[username] == password:
        print(f"Welcome Admin {username}!")
        return username
    else:
        print("Invalid admin username or password.")
        return None

# User Purchase process
def user_purchase(data, username):
    print("\n--- User Purchase ---")
    product_id = input("Enter the Product ID you want to buy: ").strip()
    if product_id not in data['Product ID'].values:
        print("Invalid Product ID.")
        return data

    product = data[data['Product ID'] == product_id].iloc[0]
    print(f"Product: {product_id}, Selling Price: ${product['Initial Price']:.2f}, Cost: ${product['Cost Price']:.2f}, Stock: {product['Stock Level']} units")

    units = int(input(f"Enter number of units to buy (Max {product['Stock Level']}): "))
    if units > product['Stock Level']:
        print("Insufficient stock!")
        return data

    data.loc[data['Product ID'] == product_id, 'Stock Level'] -= units
    data.loc[data['Product ID'] == product_id, 'Current Sales'] += units
    data.loc[data['Product ID'] == product_id, 'Total Sales'] += units
    print("Purchase successful!")

    # Update rating based on weighted average
    rating = float(input("Rate this product (1.0 to 5.0): "))
    current_sales = data.loc[data['Product ID'] == product_id, 'Current Sales'].iloc[0]
    total_sales = data.loc[data['Product ID'] == product_id, 'Total Sales'].iloc[0]
    previous_rating = data.loc[data['Product ID'] == product_id, 'Customer Rating'].iloc[0]
    updated_rating = ((previous_rating * (total_sales - units)) + (rating * units)) / total_sales
    data.loc[data['Product ID'] == product_id, 'Customer Rating'] = updated_rating
    print(f"Thank you for your feedback! The updated rating for {product_id} is {updated_rating:.2f}")
 
    save_data(data, DATA_FILE)

    return data

def random_forest_predict(data, product_id):
    features = ['Cost Price', 'Stock Level', 'Total Sales']
    target = 'Initial Price'
    data_clean = data.dropna(subset=features + [target])
    X = data_clean[features]
    y = data_clean[target]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    product_data = data[data['Product ID'] == product_id]
    predicted_price = model.predict(product_data[features])[0]
    return predicted_price

# Determine product state for Q-Learning
def get_state(row):
    if row['Current Sales'] > 100:
        return 'high_demand'
    elif 50 < row['Current Sales'] <= 100:
        return 'medium_demand'
    elif row['Current Sales'] < 10 and row['Stock Level'] > 50:
        return 'low_demand'
    elif row['Current Sales'] == 0:
        return 'no_demand'
    else:
        return 'low_demand'

# Reward calculation for Q-Learning
def calculate_reward(new_price, current_sales, cost_price):
    profit = new_price - cost_price
    if current_sales == 0:
        return -10
    return profit * current_sales

# Q-Learning Update
def update_q_table(state, action, reward, next_state):
    state_idx = state_to_index[state]
    action_idx = action_to_index[action]
    next_state_idx = state_to_index[next_state]
    best_next_action = np.max(q_table[next_state_idx])
    q_table[state_idx][action_idx] += learning_rate * (
        reward + discount_factor * best_next_action - q_table[state_idx][action_idx]
    )

# Apply actions for Q-Learning
def apply_action(row, action):
    max_price = row['Max Price']
    if action == 'increase_20':
        return min(max_price, max(row['Initial Price'] * 1.20, row['Cost Price']))
    elif action == 'increase_10':
        return min(max_price, max(row['Initial Price'] * 1.10, row['Cost Price']))
    elif action == 'decrease_10':
        return max(row['Initial Price'] * 0.90, row['Cost Price'])
    elif action == 'decrease_20':
        return max(row['Initial Price'] * 0.80, row['Cost Price'])
    else:
        return row['Initial Price']

# Admin Q-Learning Update
def admin_q_learning_update(data):
    global exploration_rate
    for index, row in data.iterrows():
        current_state = get_state(row)
        if random.random() < exploration_rate:
            action = random.choice(actions)
        else:
            state_idx = state_to_index[current_state]
            action_idx = np.argmax(q_table[state_idx])
            action = actions[action_idx]

        new_price = apply_action(row, action)
        reward = calculate_reward(new_price, row['Current Sales'], row['Cost Price'])
        next_state = get_state(row)
        update_q_table(current_state, action, reward, next_state)
        data.loc[index, 'Initial Price'] = round(new_price, 2)
        
    data['Current Sales'] = 0
    exploration_rate = max(0.1, exploration_rate * 0.99)
    print("Prices updated using Q-Learning, and current sales reset to 0.")
    save_data(data, DATA_FILE)

# Admin Add New Product process
def admin_add_new_product(data):
    product_id = input("Enter Product ID: ").strip()
    name = input("Enter Product Name: ").strip()
    initial_price = float(input("Enter Initial Price: "))
    cost_price = float(input("Enter Cost Price: "))
    max_price = float(input("Enter Max Price: "))
    stock_level = int(input("Enter Stock Level: "))
    new_product = {
        'Product ID': product_id,
        'Product Name': name,
        'Initial Price': min(initial_price, max_price),
        'Cost Price': cost_price,
        'Max Price': max_price,
        'Stock Level': stock_level,
        'Total Sales': 0,
        'Current Sales': 0,
        'Customer Rating': 0
    }
    data = data.append(new_product, ignore_index=True)
    save_data(data, DATA_FILE)
    print("New product added successfully!")
import pickle

def save_q_table(q_table, file_name='q_table.pkl'):
    with open(file_name, 'wb') as f:
        pickle.dump(q_table, f)

def load_q_table(file_name='q_table.pkl'):
    with open(file_name, 'rb') as f:
        return pickle.load(f)
    
def main():
    data = load_data(DATA_FILE)
    load_q_table()
    # Apply Random Forest to all products
    random_forest_predict_all(data)
    while True:
        print("\n1. User Login\n2. Admin Login\n3. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            username = user_login()
            if username:
                while True:
                    print("\n1. Buy Products\n2. Logout")
                    user_choice = int(input("Enter your choice: "))
                    if user_choice == 1:
                        data = user_purchase(data, username)
                    elif user_choice == 2:
                        break
                    else:
                        print("Invalid choice!")
        elif choice == 2:
            username = admin_login()
            if username:
                while True:
                    print("\n1. Update Prices (Q-Learning)\n2. Add New Product\n3. Logout")
                    admin_choice = int(input("Enter your choice: "))
                    if admin_choice == 1:
                        admin_q_learning_update(data)
                    elif admin_choice == 2:
                        admin_add_new_product(data)
                    elif admin_choice == 3:
                        break
                    else:
                        print("Invalid choice!")
        elif choice == 3:
            save_q_table(q_table)
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
