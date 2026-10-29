"""
Dirty Enterprise Data Generator for Data Cleaning & Reporting Automation.
Generates realistic raw multi-source enterprise transaction data with
common real-world data quality issues (duplicates, mixed formats, missing values,
string casing issues, currency symbols in numeric columns, and statistical anomalies).
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_dirty_data(n_records: int = 3200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    days_range = (end_date - start_date).days

    customers = [
        {"id": f"CUST-{1000 + i}", "name": name, "domain": domain}
        for i, (name, domain) in enumerate([
            ("Acme Corporation", "acme.com"),
            ("Nexus Technologies", "nexustech.io"),
            ("Apex Global Solutions", "apexsolutions.com"),
            ("Vanguard Financial", "vanguardfin.org"),
            ("Quantum Dynamics", "quantumdyn.net"),
            ("Starlight Media", "starlightmedia.com"),
            ("Horizon Logistics", "horizonlogistics.com"),
            ("Pinnacle Health", "pinnaclehealth.org"),
            ("Crestview Capital", "crestview.com"),
            ("Solaris Energy", "solarisenergy.com"),
            ("CyberShield Security", "cybershield.io"),
            ("Aura Retail Group", "auraretail.com"),
            ("Summit Cloud Systems", "summitcloud.net"),
            ("Titan Manufacturing", "titanmfg.com"),
            ("BlueWave Analytics", "bluewave.ai"),
            ("OmniCorp International", "omnicorp.com"),
            ("Velocity Software", "velocitysoft.io"),
            ("Zenith BioTech", "zenithbio.org"),
            ("Echo Systems", "echosystems.com"),
            ("Ironclad Security", "ironcladsec.io")
        ])
    ]

    clean_categories = [
        "Cloud Infrastructure",
        "Cybersecurity Suite",
        "Business Intelligence",
        "Enterprise Hardware",
        "DevOps Automation",
        "Managed Services"
    ]

    base_prices = {
        "Cloud Infrastructure": 1250.0,
        "Cybersecurity Suite": 850.0,
        "Business Intelligence": 620.0,
        "Enterprise Hardware": 3400.0,
        "DevOps Automation": 980.0,
        "Managed Services": 450.0
    }

    clean_regions = ["North America", "EMEA", "APAC", "Latin America"]

    records = []
    
    for i in range(n_records):
        cust = random.choice(customers)
        cust_id = cust["id"]
        cust_name = cust["name"]
        
        # Product Category with occasional typos / inconsistent casing
        cat_clean = random.choice(clean_categories)
        cat_noise = random.random()
        if cat_noise < 0.08:
            cat_val = cat_clean.upper()
        elif cat_noise < 0.14:
            cat_val = f"  {cat_clean.lower()}  "
        elif cat_noise < 0.18:
            typo_map = {
                "Cloud Infrastructure": "Cloud Infra",
                "Cybersecurity Suite": "Cyber Security",
                "Business Intelligence": "BI & Analytics",
                "Enterprise Hardware": "Ent Hardware",
                "DevOps Automation": "DevOps Auto",
                "Managed Services": "Managed Serv."
            }
            cat_val = typo_map[cat_clean]
        else:
            cat_val = cat_clean

        # Region with inconsistencies
        reg_clean = random.choice(clean_regions)
        reg_noise = random.random()
        if reg_noise < 0.06:
            reg_val = reg_clean.lower()
        elif reg_noise < 0.10:
            reg_map = {"North America": "NA / US", "EMEA": "Europe & ME", "APAC": "Asia Pacific", "Latin America": "LATAM"}
            reg_val = reg_map[reg_clean]
        elif reg_noise < 0.13:
            reg_val = f"{reg_clean} "
        else:
            reg_val = reg_clean

        # Order Date
        rand_days = random.randint(0, days_range)
        order_dt = start_date + timedelta(days=rand_days)
        
        # Mixed date formats
        dt_noise = random.random()
        if dt_noise < 0.10:
            order_date_str = order_dt.strftime("%d/%m/%Y")
        elif dt_noise < 0.18:
            order_date_str = order_dt.strftime("%m-%d-%Y")
        elif dt_noise < 0.23:
            order_date_str = order_dt.strftime("%Y/%m/%d %H:%M:%S")
        else:
            order_date_str = order_dt.strftime("%Y-%m-%d")

        # Ship Date (usually 2-7 days after order date, with 2% negative ship time bug)
        ship_lag = random.randint(2, 7)
        if random.random() < 0.02:
            ship_dt = order_dt - timedelta(days=random.randint(1, 5)) # chronological violation
        else:
            ship_dt = order_dt + timedelta(days=ship_lag)
        ship_date_str = ship_dt.strftime("%Y-%m-%d")

        # Order Quantity
        q_noise = random.random()
        if q_noise < 0.015:
            quantity = -1 * random.randint(1, 5) # Negative quantity error
        elif q_noise < 0.025:
            quantity = random.randint(500, 2500) # Extreme outlier
        else:
            quantity = random.randint(1, 20)

        # Unit Price
        base_p = base_prices[cat_clean]
        p_noise = random.random()
        if p_noise < 0.01:
            unit_price_val = base_p * 100.0 # Fat finger multiplier
        else:
            unit_price_val = round(base_p * random.uniform(0.9, 1.15), 2)

        # Currency formatting noise
        curr_noise = random.random()
        if curr_noise < 0.07:
            unit_price_str = f"${unit_price_val:,.2f}"
        elif curr_noise < 0.11:
            unit_price_str = f"{unit_price_val:,.2f} USD"
        elif curr_noise < 0.14:
            unit_price_str = str(unit_price_val)
        else:
            unit_price_str = unit_price_val

        # Discount
        d_noise = random.random()
        if d_noise < 0.02:
            discount = round(random.uniform(1.1, 2.5), 2) # Invalid > 100% discount
        elif d_noise < 0.15:
            discount = None # Missing discount
        else:
            discount = round(random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.25]), 2)

        # Customer Email
        email_noise = random.random()
        if email_noise < 0.04:
            cust_email = f"contact@{cust['domain'].upper()}"
        elif email_noise < 0.07:
            cust_email = f"billing_{cust['domain'].replace('.', '_')}noat.com" # Missing @
        elif email_noise < 0.10:
            cust_email = None # Missing email
        else:
            first_name = cust_name.split()[0].lower()
            cust_email = f"{first_name}@{cust['domain']}"

        # Payment Status
        pay_noise = random.random()
        if pay_noise < 0.05:
            payment_status = random.choice(["N/A", "null", "PENDING_VERIF", "?", "-999"])
        elif pay_noise < 0.10:
            payment_status = None
        else:
            payment_status = random.choice(["Paid", "Pending", "Authorized", "Refunded"])

        # Sales Rep
        sales_reps = ["Sarah Jenkins", "Michael Chang", "Elena Rostova", "David Kim", "Marcus Vance", "Laura Chen"]
        rep_noise = random.random()
        if rep_noise < 0.08:
            sales_rep = None
        elif rep_noise < 0.12:
            sales_rep = f"  {random.choice(sales_reps).upper()}  "
        else:
            sales_rep = random.choice(sales_reps)

        # Total Revenue (sometimes pre-calculated, sometimes missing or with calculation discrepancy)
        if isinstance(unit_price_val, (int, float)) and isinstance(quantity, int) and quantity > 0:
            d_eff = discount if (discount is not None and 0 <= discount <= 1) else 0.0
            calc_rev = round(quantity * unit_price_val * (1.0 - d_eff), 2)
            if random.random() < 0.03:
                total_rev = round(calc_rev * random.uniform(1.2, 1.8), 2) # Calculation mismatch
            else:
                total_rev = calc_rev
        else:
            total_rev = None

        tx_id = f"TXN-{20240000 + i}"

        records.append({
            "Transaction_ID": tx_id,
            "Order_Date": order_date_str,
            "Ship_Date": ship_date_str,
            "Customer_ID": cust_id,
            "Customer_Name": cust_name,
            "Customer_Email": cust_email,
            "Region": reg_val,
            "Product_Category": cat_val,
            "Quantity": quantity,
            "Unit_Price": unit_price_str,
            "Discount": discount,
            "Total_Revenue": total_rev,
            "Payment_Status": payment_status,
            "Sales_Representative": sales_rep
        })

    df = pd.DataFrame(records)

    # Inject exact duplicate rows (simulating duplicate webhook events / sync batches)
    n_dupes = 180
    dupe_indices = np.random.choice(len(df), size=n_dupes, replace=False)
    dupe_rows = df.iloc[dupe_indices].copy()
    df = pd.concat([df, dupe_rows], ignore_index=True)

    # Inject artificial null tokens into random cells
    null_tokens = ["N/A", "NA", "null", "None", "-999", "?", ""]
    cols_for_null_noise = ["Customer_Name", "Region", "Payment_Status", "Sales_Representative"]
    for col in cols_for_null_noise:
        noise_idx = np.random.choice(len(df), size=int(len(df) * 0.03), replace=False)
        for idx in noise_idx:
            df.at[idx, col] = random.choice(null_tokens)

    # Shuffle rows
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df

def save_dirty_dataset():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    df = generate_dirty_data(n_records=3200, seed=42)
    
    csv_path = os.path.join(output_dir, "raw_enterprise_data.csv")
    xlsx_path = os.path.join(output_dir, "raw_enterprise_data.xlsx")
    
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False, engine="openpyxl")
    
    print(f"[OK] Generated {len(df)} dirty enterprise records.")
    print(f"[OK] CSV saved to: {csv_path}")
    print(f"[OK] Excel saved to: {xlsx_path}")

if __name__ == "__main__":
    save_dirty_dataset()
