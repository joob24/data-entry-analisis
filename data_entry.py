import pandas as pd
import os

# Custom function to format USD: No comma, dot for thousands, always three decimals (.000)
def format_usd(amount):
    # Format to three decimals
    s = f"{amount:.3f}"
    if '.' not in s:
        s += '.000'
    
    # Split integer and decimal parts
    parts = s.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else '000'
    
    # Add dot thousands separator to integer part (from right, every 3 digits)
    if len(integer_part) > 3:
        rev_integer = integer_part[::-1]
        formatted_rev = '.'.join([rev_integer[i:i+3] for i in range(0, len(rev_integer), 3)])
        integer_part = formatted_rev[::-1]
    
    return f"${integer_part}.{decimal_part}"

# Function to validate and get float input
def get_float_input(prompt):
    while True:
        try:
            value = input(prompt).strip().replace(',', '')  # Remove any commas if entered
            return float(value)
        except ValueError:
            print("Error: Enter a valid number (e.g., 10.000 or 1000).")

# Main function to add entry
def add_entry():
    print("\n=== Add New Purchase Entry (in USD) ===")
    
    # Input date
    date = input("Date (YYYY-MM-DD, e.g., 2023-10-01): ").strip()
    
    # Input vendor
    vendor = input("Vendor (company name, e.g., Toko ABC): ").strip()
    
    # Input description
    description = input("Description (product name, e.g., groceries): ").strip()
    
    # Input price (USD per unit)
    price = get_float_input("Price per unit (USD, e.g., 10.000): ")
    
    # Input unit
    unit = get_float_input("Unit (quantity, e.g., 5): ")
    
    # Calculate subtotal = price * unit (USD)
    subtotal = price * unit
    
    # Calculate tax = subtotal * 12% (0.12)
    tax = subtotal * 0.12
    
    # Calculate total = subtotal + tax (USD)
    total = subtotal + tax
    
    # Display preview with custom formatting
    print(f"\nPreview Entry:")
    print(f"Date: {date}")
    print(f"Vendor: {vendor}")
    print(f"Description: {description}")
    print(f"Price: {format_usd(price)}")
    print(f"Unit: {unit}")
    print(f"Subtotal: {format_usd(subtotal)}")
    print(f"Tax (12% of subtotal): {format_usd(tax)}")
    print(f"Total: {format_usd(total)}")
    
    # Confirmation
    confirm = input("\nSave this entry? (y/n): ").strip().lower()
    if confirm == 'y':
        # Create new DataFrame
        new_entry = pd.DataFrame({
            'date': [date],
            'vendor': [vendor],
            'description': [description],
            'price': [price],
            'unit': [unit],
            'subtotal': [subtotal],
            'tax': [tax],
            'total': [total]
        })
        
        # Check CSV file
        if os.path.exists('data.csv'):
            # Append to existing CSV
            df_existing = pd.read_csv('data.csv')
            df_updated = pd.concat([df_existing, new_entry], ignore_index=True)
            df_updated.to_csv('data.csv', index=False)
            print(f"Entry saved! Total entries now: {len(df_updated)}")
        else:
            # Create new CSV
            new_entry.to_csv('data.csv', index=False)
            print("Entry saved! File data.csv created.")
    else:
        print("Entry cancelled.")

# Main menu
while True:
    print("\n=== Data Entry System (USD Currency) ===")
    print("1. Add New Entry")
    print("2. View Current Data")
    print("3. Exit")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == '1':
        add_entry()
    elif choice == '2':
        if os.path.exists('data.csv'):
            df = pd.read_csv('data.csv')
            if not df.empty:
                print("\nCurrent Data:")
                for idx, row in df.iterrows():
                    # Multi-line f-string with parentheses (fixed syntax)
                    print((
                        f"Entry {idx+1}: Date={row['date']}, Vendor={row['vendor']}, "
                        f"Description={row['description']}, "
                        f"Price={format_usd(row['price'])}, Unit={row['unit']}, "
                        f"Subtotal={format_usd(row['subtotal'])}, "
                        f"Tax={format_usd(row['tax'])}, Total={format_usd(row['total'])}"
                    ))
            else:
                print("Data is empty.")
        else:
            print("File data.csv does not exist yet. Add an entry first.")
    elif choice == '3':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Try again.")