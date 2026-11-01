import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cafe_clean.csv")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
df["Month"] = df["Transaction Date"].dt.strftime("%Y-%m")


conn = sqlite3.connect(":memory:")
df.to_sql("sales", conn, index=False)

queries = {
 "Q1 Total revenue and transactions":
   "SELECT ROUND(SUM([Total Spent]),2) AS total_revenue, COUNT(*) AS total_transactions FROM sales;",
 "Q2 Top 5 items by revenue":
   "SELECT Item, ROUND(SUM([Total Spent]),2) AS revenue FROM sales GROUP BY Item ORDER BY revenue DESC LIMIT 5;",
 "Q3 Sales by location":
   "SELECT Location, ROUND(SUM([Total Spent]),2) AS revenue FROM sales GROUP BY Location ORDER BY revenue DESC;",
 "Q4 Sales by payment method":
   "SELECT [Payment Method], COUNT(*) AS transactions, ROUND(SUM([Total Spent]),2) AS revenue FROM sales GROUP BY [Payment Method] ORDER BY revenue DESC;",
 "Q5 Average order value":
   "SELECT ROUND(AVG([Total Spent]),2) AS avg_order_value FROM sales;",
 "Q6 Revenue by month":
   "SELECT Month, ROUND(SUM([Total Spent]),2) AS revenue FROM sales GROUP BY Month ORDER BY revenue DESC;",
}
for name, q in queries.items():
    print("\n" + name)
    print(q)
    print(pd.read_sql_query(q, conn).to_string(index=False))


kpi = {
 "Total Revenue": round(df["Total Spent"].sum(), 2),
 "Total Transactions": len(df),
 "Average Order Value": round(df["Total Spent"].mean(), 2),
 "Best-selling Item (revenue)": df.groupby("Item")["Total Spent"].sum().idxmax(),
 "Lowest-selling Item (revenue)": df.groupby("Item")["Total Spent"].sum().idxmin(),
 "Best Month": df.groupby("Month")["Total Spent"].sum().idxmax(),
 "Worst Month": df.groupby("Month")["Total Spent"].sum().idxmin(),
 "Top Payment Method (known)": df[df["Payment Method"]!="Unknown"].groupby("Payment Method")["Total Spent"].sum().idxmax(),
}
print("\n===== KPI SUMMARY =====")
for k, v in kpi.items():
    print(f"{k}: {v}")
pd.Series(kpi).to_csv("task5_kpis.csv", header=["Value"])


sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(2, 2, figsize=(14, 10))

item_sales = df.groupby("Item")["Total Spent"].sum().sort_values(ascending=False)
sns.barplot(x=item_sales.index, y=item_sales.values, ax=ax[0,0])
ax[0,0].set_title("Total Sales by Item")

month_sales = df.groupby("Month")["Total Spent"].sum()
ax[0,1].plot(month_sales.index, month_sales.values, marker="o")
ax[0,1].set_title("Monthly Sales Trend")
ax[0,1].tick_params(axis="x", rotation=45)

pay = df[df["Payment Method"]!="Unknown"].groupby("Payment Method")["Total Spent"].sum()
ax[1,0].pie(pay.values, labels=pay.index, autopct="%1.1f%%")
ax[1,0].set_title("Sales Share by Payment Method")

sns.boxplot(x="Item", y="Total Spent", data=df, ax=ax[1,1])
ax[1,1].set_title("Order Value Distribution by Item")
ax[1,1].tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("task6_visualization.png", dpi=150)
print("\nSaved task6_visualization.png and task5_kpis.csv")
plt.show()