import pandas as pd
import os
import shutil

# File path for the CSV
DATA_FILE = "product_data.csv"

# Load or create the dataset
def load_data(file_path):
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        print(f"Error: File '{file_path}' does not exist.")
        exit()
    return data

# Save the updated dataset
def save_data(data, file_path):
    try:
        temp_file = file_path + ".tmp"
        data.to_csv(temp_file, index=False)  # Save to a temporary file first
        shutil.move(temp_file, file_path)  # Replace the original file
        print("Data saved successfully!")
    except PermissionError as e:
        print(f"Permission error: {e}. Please close the file if it's open and check permissions.")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# User purchase process
def user_purchase(data):
    print("\n--- User Purchase ---")
    print(data[['Product ID', 'Initial Price', 'Cost Price', 'Stock Level']])  # Show basic details

    # Get user input
    product_id = input("Enter the Product ID you want to buy: ").strip()
    if product_id not in data['Product ID'].values:
        print("Invalid Product ID.")
        return data

    product = data[data['Product ID'] == product_id].iloc[0]
    print(f"Product: {product_id}, MRP: ${product['Initial Price']:.2f}, Cost: ${product['Cost Price']:.2f}, Stock: {product['Stock Level']} units")

    # Get number of units to buy
    units = int(input(f"Enter number of units to buy (Max {product['Stock Level']}): "))
    if units > product['Stock Level']:
        print("Insufficient stock!")
        return data

    # Update stock level
    data.loc[data['Product ID'] == product_id, 'Stock Level'] -= units
    data.loc[data['Product ID'] == product_id, 'Current Sales'] += units
    data.loc[data['Product ID'] == product_id, 'Total Sales'] += units  # Update total sales
    print("Purchase successful!")

    # Get user rating
    rating = float(input("Rate this product (1.0 to 5.0): "))

    # Calculate the updated customer rating
    current_sales = data.loc[data['Product ID'] == product_id, 'Current Sales'].iloc[0]
    previous_rating = data.loc[data['Product ID'] == product_id, 'Customer Rating'].iloc[0]
    print(previous_rating,current_sales,units)
    # Weighted average formula for rating calculation
    updated_rating = ((previous_rating * (current_sales - units)) + (rating * units)) / current_sales
    
    data.loc[data['Product ID'] == product_id, 'Customer Rating'] = updated_rating
    print(f"Thank you for your feedback! The updated rating for {product_id} is {updated_rating:.2f}")

    return data

# Main program
def main():
    # Load the dataset
    data = load_data(DATA_FILE)

    while True:
        print("\n1. Buy a Product\n2. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            data = user_purchase(data)
            save_data(data, DATA_FILE)  # Save updates after every purchase
        elif choice == 2:
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()