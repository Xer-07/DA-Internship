"""
Customer Segmentation Machine Learning Pipeline
Implements RFM Feature Engineering, Standardization, Optimal K (Elbow & Silhouette),
K-Means Clustering, PCA Dimensionality Reduction, and Persona Synthesis.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA

class CustomerSegmentationPipeline:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.features_df = None
        self.scaled_features = None
        self.scaler = StandardScaler()
        self.kmeans = None
        self.optimal_k = 5
        self.evaluation_metrics = {}
        self.cluster_profiles = {}
        
        self.feature_columns = [
            "Annual_Income",
            "Spending_Score",
            "Recency_Days",
            "Frequency",
            "Monetary_Total",
            "Web_Visits_Per_Month"
        ]

    def load_and_preprocess(self):
        """Loads customer dataset and validates clean data structures"""
        self.df = pd.read_csv(self.data_path)
        print(f"[OK] Ingested {len(self.df):,} customer records from {self.data_path}")
        
        # Extract features for clustering
        self.features_df = self.df[self.feature_columns].copy()
        self.scaled_features = self.scaler.fit_transform(self.features_df)
        return self.df

    def evaluate_optimal_clusters(self, k_range=range(2, 10)):
        """Computes WCSS (Inertia) and Silhouette Scores across cluster counts"""
        wcss = []
        silhouettes = []
        calinskis = []

        for k in k_range:
            km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
            labels = km.fit_predict(self.scaled_features)
            wcss.append(float(km.inertia_))
            sil = float(silhouette_score(self.scaled_features, labels))
            ch = float(calinski_harabasz_score(self.scaled_features, labels))
            silhouettes.append(round(sil, 4))
            calinskis.append(round(ch, 2))

        self.evaluation_metrics = {
            "k_values": list(k_range),
            "wcss": [round(w, 2) for w in wcss],
            "silhouette_scores": silhouettes,
            "calinski_harabasz": calinskis
        }
        print(f"[OK] Completed Elbow & Silhouette evaluations for k in {list(k_range)}")
        return self.evaluation_metrics

    def fit_kmeans(self, k=5):
        """Trains final K-Means model and applies PCA dimensionality reduction"""
        self.optimal_k = k
        self.kmeans = KMeans(n_clusters=k, init="k-means++", n_init=20, random_state=42)
        cluster_labels = self.kmeans.fit_predict(self.scaled_features)
        self.df["Cluster"] = cluster_labels

        # Dimensionality Reduction via PCA for 2D/3D visualization
        pca = PCA(n_components=3, random_state=42)
        pca_coords = pca.fit_transform(self.scaled_features)
        self.df["PCA_1"] = np.round(pca_coords[:, 0], 3)
        self.df["PCA_2"] = np.round(pca_coords[:, 1], 3)
        self.df["PCA_3"] = np.round(pca_coords[:, 2], 3)
        
        var_ratio = pca.explained_variance_ratio_
        print(f"[OK] PCA Explained Variance (2D: {sum(var_ratio[:2])*100:.1f}%, 3D: {sum(var_ratio)*100:.1f}%)")

        self._assign_business_labels()
        self._build_cluster_profiles()
        return self.df

    def _assign_business_labels(self):
        """Assigns meaningful enterprise persona names based on cluster centroids"""
        cluster_agg = self.df.groupby("Cluster").agg(
            Avg_Income=("Annual_Income", "mean"),
            Avg_Monetary=("Monetary_Total", "mean"),
            Avg_Recency=("Recency_Days", "mean"),
            Avg_SpendingScore=("Spending_Score", "mean"),
            Avg_Frequency=("Frequency", "mean")
        )

        label_map = {}
        for c_id, row in cluster_agg.iterrows():
            inc = row["Avg_Income"]
            spend = row["Avg_Monetary"]
            rec = row["Avg_Recency"]
            score = row["Avg_SpendingScore"]

            if spend > 14000 and inc > 95000:
                label = "VIP Champions"
            elif rec > 150:
                label = "At-Risk / Lapsed"
            elif inc < 50000 and score < 50:
                label = "Bargain Hunters"
            elif score > 68 and row["Avg_Frequency"] > 16:
                label = "Emerging Tech Lovers"
            else:
                label = "Loyal Mainstream"
            label_map[c_id] = label

        self.df["Cluster_Name"] = self.df["Cluster"].map(label_map)

    def _build_cluster_profiles(self):
        """Builds comprehensive JSON summary profiles and marketing actions"""
        total_cust = len(self.df)
        total_rev = self.df["Monetary_Total"].sum()

        marketing_playbook = {
            "VIP Champions": {
                "Strategy": "Retention & Exclusive Privileges",
                "Action": "Provide dedicated concierge account managers, preview access to new product releases, zero-threshold free shipping, and luxury loyalty tier recognition.",
                "Channel": "Personal Email, Concierge SMS, Executive Invitations",
                "Color": "#10B981"
            },
            "Loyal Mainstream": {
                "Strategy": "Upsell & Category Expansion",
                "Action": "Cross-sell complementary categories (e.g. bundling office supplies with furniture), offer multi-buy bundle discounts, and encourage annual subscription renewals.",
                "Channel": "Automated Email Drips, In-App Banners",
                "Color": "#3B82F6"
            },
            "Emerging Tech Lovers": {
                "Strategy": "Early Adoption & Feature Advocacy",
                "Action": "Target with cutting-edge gadget launches, tech bundle pre-orders, interactive web webinars, and gamified loyalty point multipliers.",
                "Channel": "Push Notifications, Social Retargeting, Tech Newsletters",
                "Color": "#8B5CF6"
            },
            "Bargain Hunters": {
                "Strategy": "Volume Conversions & Price Elasticity",
                "Action": "Promote flash sales, clearance outlets, seasonal promo codes, and free gift-with-purchase incentives on overstocked SKUs.",
                "Channel": "Promotional SMS, Discount Banners, Coupon Aggregators",
                "Color": "#F59E0B"
            },
            "At-Risk / Lapsed": {
                "Strategy": "Re-Activation & Churn Mitigation",
                "Action": "Deploy aggressive 'We miss you' win-back campaigns offering 20% off renewal, conduct customer satisfaction exit surveys, and resolve service friction points.",
                "Channel": "Personalized Win-Back Email, Direct Mail Coupon",
                "Color": "#EF4444"
            }
        }

        profiles = []
        for c_id in sorted(self.df["Cluster"].unique()):
            sub = self.df[self.df["Cluster"] == c_id]
            name = sub["Cluster_Name"].iloc[0]
            playbook = marketing_playbook.get(name, {
                "Strategy": "Growth",
                "Action": "Standard marketing engagement",
                "Channel": "Omnichannel",
                "Color": "#6B7280"
            })

            profile = {
                "Cluster_ID": int(c_id),
                "Persona_Name": name,
                "Customer_Count": int(len(sub)),
                "Percentage_Share": round(len(sub) / total_cust * 100, 2),
                "Total_Monetary_Spend": round(float(sub["Monetary_Total"].sum()), 2),
                "Revenue_Contribution_Pct": round(float(sub["Monetary_Total"].sum()) / total_rev * 100, 2),
                "Avg_Annual_Income": round(float(sub["Annual_Income"].mean()), 2),
                "Avg_Spending_Score": round(float(sub["Spending_Score"].mean()), 1),
                "Avg_Recency_Days": round(float(sub["Recency_Days"].mean()), 1),
                "Avg_Frequency": round(float(sub["Frequency"].mean()), 1),
                "Avg_Monetary_Spend": round(float(sub["Monetary_Total"].mean()), 2),
                "Avg_Order_Value": round(float(sub["AOV"].mean()), 2),
                "Avg_Web_Visits": round(float(sub["Web_Visits_Per_Month"].mean()), 1),
                "Top_Preferred_Category": sub["Preferred_Category"].mode().iloc[0],
                "Loyalty_Member_Pct": round((sub["Loyalty_Member"] == "Yes").mean() * 100, 1),
                "Marketing_Strategy": playbook["Strategy"],
                "Recommended_Action": playbook["Action"],
                "Marketing_Channel": playbook["Channel"],
                "Brand_Color": playbook["Color"]
            }
            profiles.append(profile)

        self.cluster_profiles = {
            "Total_Customers": total_cust,
            "Total_Revenue": round(total_rev, 2),
            "Optimal_K": self.optimal_k,
            "Profiles": profiles
        }

    def export_results(self, processed_dir):
        """Exports segmented customer CSV and cluster JSON metrics"""
        os.makedirs(processed_dir, exist_ok=True)
        
        # 1. Processed CSV
        csv_out = os.path.join(processed_dir, "segmented_customers.csv")
        self.df.to_csv(csv_out, index=False)
        print(f"[OK] Saved Segmented Customers CSV: {csv_out}")

        # 2. Evaluation metrics JSON (Elbow & Silhouette)
        eval_out = os.path.join(processed_dir, "elbow_silhouette_metrics.json")
        with open(eval_out, "w", encoding="utf-8") as f:
            json.dump(self.evaluation_metrics, f, indent=2)
        print(f"[OK] Saved Clustering Evaluation Metrics: {eval_out}")

        # 3. Cluster profiles JSON
        profiles_out = os.path.join(processed_dir, "cluster_profiles_summary.json")
        with open(profiles_out, "w", encoding="utf-8") as f:
            json.dump(self.cluster_profiles, f, indent=2)
        print(f"[OK] Saved Cluster Profiles Summary: {profiles_out}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    raw_csv = os.path.join(project_root, "data", "raw", "customer_data.csv")
    proc_dir = os.path.join(project_root, "data", "processed")

    pipeline = CustomerSegmentationPipeline(raw_csv)
    pipeline.load_and_preprocess()
    pipeline.evaluate_optimal_clusters(k_range=range(2, 10))
    pipeline.fit_kmeans(k=5)
    pipeline.export_results(proc_dir)

    print("\n--- CLUSTER PROFILES SNAPSHOT ---")
    for p in pipeline.cluster_profiles["Profiles"]:
        print(f"Cluster {p['Cluster_ID']} [{p['Persona_Name']:<22}]: {p['Customer_Count']:>4} users ({p['Percentage_Share']}%) | Avg Spend: ${p['Avg_Monetary_Spend']:>9,.2f} | Strategy: {p['Marketing_Strategy']}")
