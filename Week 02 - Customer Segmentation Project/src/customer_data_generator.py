"""
Customer Analytics & Segmentation Dataset Generator
Synthesizes a realistic 2,000-customer multi-dimensional behavioral & demographic dataset
with distinct latent personas for unsupervised clustering (K-Means / PCA).
"""

import os
import random
import numpy as np
import pandas as pd

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

def generate_customer_dataset(num_customers=2000):
    first_names = ["Marcus", "Elena", "Devon", "Chloe", "Julian", "Aaliyah", "Lucas", "Maya", "Nathan", "Zoe",
                   "Alexander", "Leila", "Darius", "Sienna", "Ethan", "Aria", "Kai", "Nadia", "Leo", "Talia",
                   "Ganesh", "Priya", "Rahul", "Ananya", "Arjun", "Sneha", "Vikram", "Kavita", "Rohan", "Pooja",
                   "Carlos", "Sofia", "Mateo", "Camila", "Diego", "Valentina", "Kenji", "Yuki", "Hiroshi", "Mei"]
    last_names = ["Vance", "Mercer", "Chen", "Sterling", "Cross", "Novak", "Sinclair", "Hawthorne", "Delgado", "Kovacs",
                  "Patel", "Sharma", "Verma", "Rao", "Reddy", "Nair", "Kapoor", "Mehta", "Iyer", "Choudhury",
                  "Silva", "Santos", "Tanaka", "Yamamoto", "Watanabe", "Kim", "Park", "Choi", "Zhang", "Wang"]

    cities_by_region = {
        "West": ["Los Angeles", "San Francisco", "Seattle", "San Diego", "Portland"],
        "East": ["New York City", "Boston", "Philadelphia", "Washington D.C."],
        "Central": ["Chicago", "Austin", "Dallas", "Houston", "Denver"],
        "South": ["Atlanta", "Miami", "Orlando", "Charlotte", "Nashville"]
    }
    
    categories = ["Technology", "Furniture", "Office Supplies", "Fashion & Apparel", "Home & Kitchen"]

    # Defined Persona Distributions
    # 1. VIP Champions (18%)
    # 2. Loyal Mainstream (28%)
    # 3. Emerging Tech Enthusiasts (20%)
    # 4. Bargain Hunters (22%)
    # 5. At-Risk / Lapsed Customers (12%)
    persona_types = ["VIP Champion", "Loyal Mainstream", "Tech Enthusiast", "Bargain Hunter", "At Risk"]
    persona_weights = [0.18, 0.28, 0.20, 0.22, 0.12]

    customers = []
    for i in range(num_customers):
        cid = f"CUST-{2001 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        gender = random.choices(["Female", "Male", "Non-Binary"], weights=[0.49, 0.48, 0.03])[0]
        region = random.choices(["West", "East", "Central", "South"], weights=[0.32, 0.28, 0.23, 0.17])[0]
        city = random.choice(cities_by_region[region])

        persona = random.choices(persona_types, weights=persona_weights)[0]

        if persona == "VIP Champion":
            age = int(np.random.normal(44, 9))
            income = round(float(np.random.normal(122000, 16000)), 2)
            spending_score = int(np.random.normal(86, 7))
            recency = int(np.random.exponential(14)) + 2
            frequency = int(np.random.normal(26, 5))
            monetary = round(float(np.random.normal(18500, 3200)), 2)
            preferred_cat = random.choices(categories, weights=[0.45, 0.30, 0.10, 0.10, 0.05])[0]
            web_visits = int(np.random.normal(18, 4))
            discount_sens = "Low"
            loyalty_member = random.choices(["Yes", "No"], weights=[0.92, 0.08])[0]
            tenure = int(np.random.normal(46, 12))

        elif persona == "Loyal Mainstream":
            age = int(np.random.normal(41, 11))
            income = round(float(np.random.normal(76000, 12000)), 2)
            spending_score = int(np.random.normal(62, 8))
            recency = int(np.random.exponential(28)) + 5
            frequency = int(np.random.normal(15, 3))
            monetary = round(float(np.random.normal(7400, 1500)), 2)
            preferred_cat = random.choices(categories, weights=[0.25, 0.25, 0.25, 0.15, 0.10])[0]
            web_visits = int(np.random.normal(12, 3))
            discount_sens = "Medium"
            loyalty_member = random.choices(["Yes", "No"], weights=[0.68, 0.32])[0]
            tenure = int(np.random.normal(34, 14))

        elif persona == "Tech Enthusiast":
            age = int(np.random.normal(28, 5))
            income = round(float(np.random.normal(68000, 14000)), 2)
            spending_score = int(np.random.normal(74, 9))
            recency = int(np.random.exponential(20)) + 3
            frequency = int(np.random.normal(18, 4))
            monetary = round(float(np.random.normal(8900, 2000)), 2)
            preferred_cat = "Technology"
            web_visits = int(np.random.normal(24, 5))
            discount_sens = "Medium"
            loyalty_member = random.choices(["Yes", "No"], weights=[0.75, 0.25])[0]
            tenure = int(np.random.normal(22, 8))

        elif persona == "Bargain Hunter":
            age = int(np.random.normal(36, 12))
            income = round(float(np.random.normal(38000, 9000)), 2)
            spending_score = int(np.random.normal(36, 9))
            recency = int(np.random.exponential(45)) + 10
            frequency = int(np.random.normal(9, 3))
            monetary = round(float(np.random.normal(2100, 600)), 2)
            preferred_cat = random.choices(categories, weights=[0.10, 0.15, 0.40, 0.20, 0.15])[0]
            web_visits = int(np.random.normal(19, 6))
            discount_sens = "High"
            loyalty_member = random.choices(["Yes", "No"], weights=[0.35, 0.65])[0]
            tenure = int(np.random.normal(18, 10))

        else: # At Risk
            age = int(np.random.normal(51, 10))
            income = round(float(np.random.normal(88000, 18000)), 2)
            spending_score = int(np.random.normal(24, 7))
            recency = int(np.random.normal(210, 35))
            frequency = int(np.random.normal(6, 2))
            monetary = round(float(np.random.normal(3800, 1100)), 2)
            preferred_cat = random.choices(categories, weights=[0.30, 0.35, 0.15, 0.10, 0.10])[0]
            web_visits = int(np.random.normal(4, 2))
            discount_sens = "Low"
            loyalty_member = random.choices(["Yes", "No"], weights=[0.40, 0.60])[0]
            tenure = int(np.random.normal(48, 12))

        # Clamp physical bounds
        age = max(18, min(76, age))
        income = max(18000.0, min(175000.0, income))
        spending_score = max(1, min(100, spending_score))
        recency = max(1, min(365, recency))
        frequency = max(1, min(50, frequency))
        monetary = max(250.0, min(35000.0, monetary))
        web_visits = max(1, min(40, web_visits))
        tenure = max(2, min(84, tenure))
        aov = round(monetary / frequency, 2)
        return_rate = round(float(random.uniform(1.5, 12.0) if discount_sens != "High" else random.uniform(5.0, 22.0)), 1)

        customers.append({
            "Customer_ID": cid,
            "Customer_Name": name,
            "Gender": gender,
            "Age": age,
            "Region": region,
            "City": city,
            "Annual_Income": income,
            "Spending_Score": spending_score,
            "Recency_Days": recency,
            "Frequency": frequency,
            "Monetary_Total": monetary,
            "AOV": aov,
            "Tenure_Months": tenure,
            "Preferred_Category": preferred_cat,
            "Web_Visits_Per_Month": web_visits,
            "Discount_Sensitivity": discount_sens,
            "Loyalty_Member": loyalty_member,
            "Return_Rate_Pct": return_rate,
            "True_Archetype": persona  # Retained as baseline ground-truth
        })

    df = pd.DataFrame(customers)
    return df

def save_customer_datasets(base_path):
    raw_dir = os.path.join(base_path, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    print("Generating enterprise customer segmentation dataset...")
    df = generate_customer_dataset(num_customers=2000)

    csv_path = os.path.join(raw_dir, "customer_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"[OK] Saved Customer CSV: {csv_path} ({len(df):,} records)")

    excel_path = os.path.join(raw_dir, "customer_data.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Customer_Profiles", index=False)
        demog_summary = df.groupby("Region").agg(
            Customer_Count=("Customer_ID", "count"),
            Avg_Income=("Annual_Income", "mean"),
            Avg_Monetary=("Monetary_Total", "mean")
        ).reset_index()
        demog_summary.to_excel(writer, sheet_name="Regional_Summary", index=False)
    print(f"[OK] Saved Customer Multi-Sheet Excel: {excel_path}")

    return df

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    df = save_customer_datasets(project_root)
    print(f"Customer Count: {len(df):,}")
    print(f"Mean Annual Income: ${df['Annual_Income'].mean():,.2f}")
    print(f"Mean Monetary Spend: ${df['Monetary_Total'].mean():,.2f}")
    print(f"Mean Spending Score: {df['Spending_Score'].mean():.1f}/100")
