"""
Realistic Enterprise Sales and Revenue Dataset Generator
Generates multi-year sales transactions with realistic business distributions,
seasonal spikes, product hierarchies, and financial metrics.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

def generate_sales_dataset(num_records=3500):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 10, 15)
    total_days = (end_date - start_date).days

    # Master Product Catalog
    catalog = [
        # Technology
        {"Category": "Technology", "Sub_Category": "Laptops & Computers", "Product_Name": "Dell XPS 15 InfinityEdge Laptop", "Cost": 1150.00, "Price": 1699.99},
        {"Category": "Technology", "Sub_Category": "Laptops & Computers", "Product_Name": "Apple MacBook Pro 16-inch M3", "Cost": 1750.00, "Price": 2499.00},
        {"Category": "Technology", "Sub_Category": "Laptops & Computers", "Product_Name": "Lenovo ThinkPad X1 Carbon Gen 11", "Cost": 980.00, "Price": 1420.00},
        {"Category": "Technology", "Sub_Category": "Phones & Tablets", "Product_Name": "Apple iPhone 15 Pro Max 256GB", "Cost": 780.00, "Price": 1199.00},
        {"Category": "Technology", "Sub_Category": "Phones & Tablets", "Product_Name": "Samsung Galaxy S24 Ultra", "Cost": 740.00, "Price": 1249.99},
        {"Category": "Technology", "Sub_Category": "Phones & Tablets", "Product_Name": "Google Pixel 8 Pro", "Cost": 580.00, "Price": 899.00},
        {"Category": "Technology", "Sub_Category": "Peripherals & Accessories", "Product_Name": "Logitech MX Master 3S Wireless Mouse", "Cost": 55.00, "Price": 99.99},
        {"Category": "Technology", "Sub_Category": "Peripherals & Accessories", "Product_Name": "Dell UltraSharp 32-inch 4K USB-C Monitor", "Cost": 420.00, "Price": 679.00},
        {"Category": "Technology", "Sub_Category": "Peripherals & Accessories", "Product_Name": "Keychron Q3 Pro Mechanical Keyboard", "Cost": 110.00, "Price": 189.00},
        {"Category": "Technology", "Sub_Category": "Networking & Storage", "Product_Name": "Cisco Catalyst 24-Port Gigabit Switch", "Cost": 620.00, "Price": 950.00},
        {"Category": "Technology", "Sub_Category": "Networking & Storage", "Product_Name": "Synology DiskStation DS923+ 4-Bay NAS", "Cost": 360.00, "Price": 599.99},
        {"Category": "Technology", "Sub_Category": "Audio & Video", "Product_Name": "Sony WH-1000XM5 Noise Canceling Headphones", "Cost": 220.00, "Price": 398.00},
        {"Category": "Technology", "Sub_Category": "Audio & Video", "Product_Name": "Jabra Speak 750 Bluetooth Speakerphone", "Cost": 160.00, "Price": 285.00},
        
        # Furniture
        {"Category": "Furniture", "Sub_Category": "Office Chairs", "Product_Name": "Herman Miller Aeron Ergonomic Chair", "Cost": 850.00, "Price": 1395.00},
        {"Category": "Furniture", "Sub_Category": "Office Chairs", "Product_Name": "Steelcase Gesture Executive Task Chair", "Cost": 790.00, "Price": 1280.00},
        {"Category": "Furniture", "Sub_Category": "Office Chairs", "Product_Name": "Ergohuman High-Back Mesh Swivel Chair", "Cost": 380.00, "Price": 620.00},
        {"Category": "Furniture", "Sub_Category": "Desks & Workstations", "Product_Name": "Jarvis Motorized Standing Desk 60x30", "Cost": 420.00, "Price": 749.00},
        {"Category": "Furniture", "Sub_Category": "Desks & Workstations", "Product_Name": "Uplift V2 Commercial Dual-Motor Desk", "Cost": 460.00, "Price": 829.00},
        {"Category": "Furniture", "Sub_Category": "Desks & Workstations", "Product_Name": "Tribesigns Executive Double Pedestal Desk", "Cost": 280.00, "Price": 499.00},
        {"Category": "Furniture", "Sub_Category": "Storage & Bookcases", "Product_Name": "Bush Furniture Cabot 5-Shelf Bookcase", "Cost": 110.00, "Price": 219.00},
        {"Category": "Furniture", "Sub_Category": "Storage & Bookcases", "Product_Name": "HON Brigade 4-Drawer Lateral File Cabinet", "Cost": 350.00, "Price": 599.00},
        {"Category": "Furniture", "Sub_Category": "Lighting & Decor", "Product_Name": "BenQ ScreenBar Halo LED Monitor Light", "Cost": 95.00, "Price": 179.00},
        {"Category": "Furniture", "Sub_Category": "Lighting & Decor", "Product_Name": "Steelcase Personal Task Ambient Light", "Cost": 80.00, "Price": 145.00},

        # Office Supplies
        {"Category": "Office Supplies", "Sub_Category": "Paper & Printing", "Product_Name": "Hammermill Premium Multi-Purpose Paper (10 Reams)", "Cost": 38.00, "Price": 64.99},
        {"Category": "Office Supplies", "Sub_Category": "Paper & Printing", "Product_Name": "HP LaserJet High Yield Black Toner Cartridge", "Cost": 115.00, "Price": 189.99},
        {"Category": "Office Supplies", "Sub_Category": "Binders & Filing", "Product_Name": "Wilson Jones Heavy Duty D-Ring 3-Inch Binder", "Cost": 8.50, "Price": 18.99},
        {"Category": "Office Supplies", "Sub_Category": "Binders & Filing", "Product_Name": "Pendaflex Hanging File Folders (Box of 50)", "Cost": 14.00, "Price": 27.50},
        {"Category": "Office Supplies", "Sub_Category": "Desk Organization", "Product_Name": "Fellowes Bankers Box Storage Organizer", "Cost": 22.00, "Price": 44.00},
        {"Category": "Office Supplies", "Sub_Category": "Desk Organization", "Product_Name": "Mind Reader Mesh Desk Organizer Caddy", "Cost": 9.50, "Price": 22.99},
        {"Category": "Office Supplies", "Sub_Category": "Writing & Markers", "Product_Name": "Pilot G2 Premium Gel Pens (Pack of 36)", "Cost": 18.00, "Price": 35.50},
        {"Category": "Office Supplies", "Sub_Category": "Writing & Markers", "Product_Name": "Expo Low Odor Dry Erase Chisel Markers (Pack of 12)", "Cost": 11.00, "Price": 23.40},
        {"Category": "Office Supplies", "Sub_Category": "Breakroom Supplies", "Product_Name": "Keurig K-Cup Coffee Variety Pack (72 Count)", "Cost": 26.00, "Price": 48.99},
    ]

    # Geography mapping
    geography = [
        {"Region": "West", "State": "California", "City": "Los Angeles", "Postal_Code": "90001"},
        {"Region": "West", "State": "California", "City": "San Francisco", "Postal_Code": "94102"},
        {"Region": "West", "State": "Washington", "City": "Seattle", "Postal_Code": "98101"},
        {"Region": "West", "State": "Oregon", "City": "Portland", "Postal_Code": "97201"},
        {"Region": "East", "State": "New York", "City": "New York City", "Postal_Code": "10001"},
        {"Region": "East", "State": "New York", "City": "Albany", "Postal_Code": "12201"},
        {"Region": "East", "State": "Massachusetts", "City": "Boston", "Postal_Code": "02108"},
        {"Region": "East", "State": "Pennsylvania", "City": "Philadelphia", "Postal_Code": "19102"},
        {"Region": "Central", "State": "Illinois", "City": "Chicago", "Postal_Code": "60601"},
        {"Region": "Central", "State": "Texas", "City": "Austin", "Postal_Code": "73301"},
        {"Region": "Central", "State": "Texas", "City": "Dallas", "Postal_Code": "75201"},
        {"Region": "Central", "State": "Texas", "City": "Houston", "Postal_Code": "77001"},
        {"Region": "Central", "State": "Michigan", "City": "Detroit", "Postal_Code": "48201"},
        {"Region": "South", "State": "Florida", "City": "Miami", "Postal_Code": "33101"},
        {"Region": "South", "State": "Florida", "City": "Orlando", "Postal_Code": "32801"},
        {"Region": "South", "State": "Georgia", "City": "Atlanta", "Postal_Code": "30301"},
        {"Region": "South", "State": "North Carolina", "City": "Charlotte", "Postal_Code": "28202"}
    ]

    # Realistic Customer Pool (450 customers)
    first_names = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "Benjamin", "Isabella", 
                   "Lucas", "Mia", "Henry", "Charlotte", "Alexander", "Amelia", "Michael", "Harper", "Ethan", "Evelyn",
                   "Daniel", "Abigail", "Matthew", "Emily", "Aiden", "Elizabeth", "David", "Mila", "Joseph", "Ella",
                   "Samuel", "Avery", "Sebastian", "Sofia", "Jack", "Camila", "Owen", "Aria", "John", "Scarlett",
                   "Ganesh", "Priya", "Rahul", "Ananya", "Arjun", "Sneha", "Vikram", "Kavita", "Rohan", "Pooja"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                  "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                  "Patel", "Sharma", "Verma", "Rao", "Reddy", "Nair", "Kapoor", "Mehta", "Iyer", "Choudhury"]
    
    customers = []
    for cid in range(1001, 1451):
        cname = f"{random.choice(first_names)} {random.choice(last_names)}"
        seg = random.choices(["Consumer", "Corporate", "Home Office"], weights=[0.52, 0.31, 0.17])[0]
        customers.append({"Customer_ID": f"CUST-{cid}", "Customer_Name": cname, "Segment": seg})

    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_weights = [0.60, 0.20, 0.15, 0.05]
    payment_methods = ["Credit Card", "Direct Wire", "PayPal", "Corporate ACH"]
    payment_weights = [0.48, 0.22, 0.18, 0.12]

    records = []
    for i in range(num_records):
        order_num = 10001 + i
        order_id = f"ORD-{order_num}"

        # Date with seasonal Q4 multiplier (more orders in Oct-Dec)
        day_offset = random.randint(0, total_days)
        cand_date = start_date + timedelta(days=day_offset)
        # Seasonal boost: Nov/Dec holiday push
        if cand_date.month in [11, 12] and random.random() < 0.28:
            # bias towards Nov/Dec
            cand_date = cand_date
        
        order_date = cand_date
        ship_lag = random.choices([1, 2, 3, 4, 5, 7], weights=[0.1, 0.25, 0.35, 0.18, 0.08, 0.04])[0]
        ship_date = order_date + timedelta(days=ship_lag)

        customer = random.choice(customers)
        geo = random.choice(geography)
        prod = random.choice(catalog)
        
        # Product ID hash
        prod_prefix = prod["Category"][:3].upper()
        prod_sub = prod["Sub_Category"][:2].upper()
        prod_id = f"{prod_prefix}-{prod_sub}-{random.randint(100, 999)}"

        ship_mode = random.choices(ship_modes, weights=ship_weights)[0]
        payment = random.choices(payment_methods, weights=payment_weights)[0]

        # Quantity depends somewhat on Segment
        if customer["Segment"] == "Corporate":
            quantity = random.choices(range(1, 15), weights=[0.1, 0.15, 0.18, 0.15, 0.12, 0.1, 0.06, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01])[0]
        elif customer["Segment"] == "Home Office":
            quantity = random.choices(range(1, 8), weights=[0.3, 0.3, 0.18, 0.1, 0.06, 0.04, 0.02])[0]
        else: # Consumer
            quantity = random.choices(range(1, 6), weights=[0.45, 0.3, 0.14, 0.07, 0.04])[0]

        # Discount policy
        discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20, 0.30], weights=[0.55, 0.15, 0.14, 0.08, 0.05, 0.03])[0]
        
        unit_price = prod["Price"]
        unit_cost = prod["Cost"]
        
        gross_sales = round(unit_price * quantity, 2)
        discount_amount = round(gross_sales * discount, 2)
        revenue = round(gross_sales - discount_amount, 2)
        cogs = round(unit_cost * quantity, 2)
        profit = round(revenue - cogs, 2)
        profit_margin = round((profit / revenue) * 100, 2) if revenue > 0 else 0.0

        records.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Ship_Date": ship_date.strftime("%Y-%m-%d"),
            "Ship_Mode": ship_mode,
            "Customer_ID": customer["Customer_ID"],
            "Customer_Name": customer["Customer_Name"],
            "Segment": customer["Segment"],
            "Country": "United States",
            "Region": geo["Region"],
            "State": geo["State"],
            "City": geo["City"],
            "Postal_Code": geo["Postal_Code"],
            "Product_ID": prod_id,
            "Category": prod["Category"],
            "Sub_Category": prod["Sub_Category"],
            "Product_Name": prod["Product_Name"],
            "Unit_Cost": unit_cost,
            "Unit_Price": unit_price,
            "Quantity": quantity,
            "Discount_Rate": discount,
            "Gross_Sales": gross_sales,
            "Discount_Amount": discount_amount,
            "Revenue": revenue,
            "COGS": cogs,
            "Profit": profit,
            "Profit_Margin_Pct": profit_margin,
            "Payment_Method": payment,
            "Order_Status": "Delivered" if ship_date < datetime(2026, 10, 1) else "Shipped"
        })

    df = pd.DataFrame(records)
    # Sort chronologically by Order_Date
    df["Order_Date_dt"] = pd.to_datetime(df["Order_Date"])
    df = df.sort_values(by="Order_Date_dt").reset_index(drop=True)
    df = df.drop(columns=["Order_Date_dt"])
    
    return df, catalog, geography

def save_datasets(base_path):
    raw_dir = os.path.join(base_path, "data", "raw")
    processed_dir = os.path.join(base_path, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    print("Generating synthetic enterprise sales dataset...")
    df, catalog, geography = generate_sales_dataset(num_records=3500)

    csv_path = os.path.join(raw_dir, "sales_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"[OK] Saved Raw CSV: {csv_path} ({len(df):,} records)")

    excel_path = os.path.join(raw_dir, "sales_data.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Sales_Transactions", index=False)
        pd.DataFrame(catalog).to_excel(writer, sheet_name="Product_Catalog", index=False)
        regional_leads = pd.DataFrame([
            {"Region": "West", "Regional_VP": "Marcus Vance", "Target_Annual_Revenue": 1500000},
            {"Region": "East", "Regional_VP": "Eleanor Brooks", "Target_Annual_Revenue": 1800000},
            {"Region": "Central", "Regional_VP": "David Zhang", "Target_Annual_Revenue": 1350000},
            {"Region": "South", "Regional_VP": "Camille Rodriguez", "Target_Annual_Revenue": 1100000},
        ])
        regional_leads.to_excel(writer, sheet_name="Regional_Targets", index=False)
    print(f"[OK] Saved Multi-Sheet Raw Excel: {excel_path}")

    # Generate Processed / Cleaned version
    cleaned_csv_path = os.path.join(processed_dir, "cleaned_sales_data.csv")
    df.to_csv(cleaned_csv_path, index=False)
    print(f"[OK] Saved Processed Cleaned CSV: {cleaned_csv_path}")

    return df

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    df = save_datasets(project_root)
    print(f"Total Revenue generated: ${df['Revenue'].sum():,.2f}")
    print(f"Total Profit generated: ${df['Profit'].sum():,.2f}")
    print(f"Average Profit Margin: {df['Profit_Margin_Pct'].mean():.2f}%")
