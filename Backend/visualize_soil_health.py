import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

# Load CSV
csv_path = "reports/soil_health_results.csv"
df = pd.read_csv(csv_path)

# Set plot style
sns.set(style="whitegrid")

# ----------------------------
# 1️⃣ Bar chart: Soil Health Scores by City
# ----------------------------
plt.figure(figsize=(12,6))
sns.barplot(x="name", y="health_score", data=df, palette="viridis")
plt.title("Soil Health Scores by City")
plt.xlabel("name")
plt.ylabel("Health Score (%)")
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.tight_layout()
bar_chart_path = "reports/soil_health_scores.png"
plt.savefig(bar_chart_path)
plt.show()
print(f"✅ Bar chart saved as: {bar_chart_path}")

# ----------------------------
# 2️⃣ Scatter plot: NDVI vs Soil Health Score
# ----------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(x="ndvi", y="health_score", hue="name", data=df, s=100, palette="tab10")
plt.title("NDVI vs Soil Health Score")
plt.xlabel("NDVI")
plt.ylabel("Health Score (%)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
scatter_plot_path = "reports/ndvi_vs_health_score.png"
plt.savefig(scatter_plot_path)
plt.show()
print(f"✅ Scatter plot saved as: {scatter_plot_path}")
