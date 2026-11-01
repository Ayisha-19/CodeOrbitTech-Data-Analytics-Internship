import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cafe.csv")
print("Raw shape:", df.shape)

# ---------- CLEANING ----------
# 1. Placeholder text becomes missing value
df = df.replace(["ERROR", "UNKNOWN"], np.nan)

# 2. Fix data types
for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")

# 3. Rebuild Total Spent from Quantity x Price where it is missing
df["Total Spent"] = df["Total Spent"].fillna(df["Quantity"] * df["Price Per Unit"])

# 4. Keep Payment Method and Location rows, label the unknowns
df["Payment Method"] = df["Payment Method"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")

# 5. Remove duplicates and rows that still cannot be used
df = df.drop_duplicates(subset="Transaction ID")
df = df.dropna(subset=["Item", "Total Spent", "Transaction Date"])

print("Clean shape:", df.shape)
print(df.isnull().sum())
df.to_csv("cafe_clean.csv", index=False)

# ---------- ANALYSIS ----------
print("\nTotal sales:", df["Total Spent"].sum())

by_item = df.groupby("Item")["Total Spent"].sum().sort_values(ascending=False)
print("\nSales by item:\n", by_item)

by_payment = df.groupby("Payment Method")["Total Spent"].sum().sort_values(ascending=False)
print("\nSales by payment method:\n", by_payment)

by_location = df.groupby("Location")["Total Spent"].sum()
print("\nSales by location:\n", by_location)

df["Month"] = df["Transaction Date"].dt.to_period("M").astype(str)
by_month = df.groupby("Month")["Total Spent"].sum()
print("\nSales by month:\n", by_month)

# ---------- CHARTS ----------
plt.figure(figsize=(8, 5))
sns.barplot(x=by_item.index, y=by_item.values)
plt.title("Total Sales by Item")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("task2_chart1_items.png")

plt.figure(figsize=(9, 5))
plt.plot(by_month.index, by_month.values, marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Sales")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("task2_chart2_monthly.png")

plt.show()