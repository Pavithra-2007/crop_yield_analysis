import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("crop_yield_data.csv")  # change filename if needed

# Show basic info
print(df.head())
print(df.describe())

# -------------------------------
# 1. Yield Trend Over Time
# -------------------------------
plt.figure()
sns.lineplot(data=df, x='Year', y='Yield_kg_per_ha', hue='Crop')
plt.title("Crop Yield Trends Over Time")
plt.savefig("Chart1_yield_trends.png")
plt.close()

# -------------------------------
# 2. Regional Comparison
# -------------------------------
plt.figure()
sns.barplot(data=df, x='Region', y='Yield_kg_per_ha', estimator=np.mean)
plt.title("Average Yield by Region")
plt.savefig("Chart2_regional.png")
plt.close()

# -------------------------------
# 3. Seasonal Heatmap
# -------------------------------
pivot = df.pivot_table(values='Yield_kg_per_ha', index='Season', columns='Crop')

plt.figure()
sns.heatmap(pivot, annot=True, cmap='coolwarm')
plt.title("Seasonal Heatmap")
plt.savefig("Chart3_seasonal_heatmap.png")
plt.close()

# -------------------------------
# 4. Seasonal Bar Chart
# -------------------------------
plt.figure()
sns.barplot(data=df, x='Season', y='Yield_kg_per_ha')
plt.title("Seasonal Yield Comparison")
plt.savefig("Chart4_seasonal_bars.png")
plt.close()

# -------------------------------
# 5. Year-over-Year Change
# -------------------------------
df['YoY_Change'] = df.groupby('Crop')['Yield_kg_per_ha'].pct_change()

plt.figure()
sns.lineplot(data=df, x='Year', y='YoY_Change', hue='Crop')
plt.title("Year-over-Year Yield Change")
plt.savefig("Chart5_yoy_change.png")
plt.close()

# -------------------------------
# 6. Drought Impact (if column exists)
# -------------------------------
if 'Drought' in df.columns:
    plt.figure()
    sns.boxplot(data=df, x='Drought', y='Yield_kg_per_ha')
    plt.title("Drought Impact on Yield")
    plt.savefig("Chart6_drought_impact.png")
    plt.close()

print("All charts generated successfully!")
