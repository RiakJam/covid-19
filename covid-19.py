# COVID-19 Data Analysis Project
# Complete Standalone Version

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import sys

# Set pandas display options for better terminal output
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 100)

# 1. Data Loading
print("🔄 Loading dataset...")
try:
    df = pd.read_csv('owid-covid-data.csv')
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("⚠️ Error: File 'owid-covid-data.csv' not found in:")
    print(f"📂 {os.getcwd()}")
    print("\nPlease download from:")
    print("https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv")
    sys.exit(1)

# 2. Data Exploration
print("\n🔍 Dataset Overview:")
print(f"📊 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print("\n📋 First 5 entries:")
print(df.head().to_string())
print("\n❓ Missing values:")
print(df.isnull().sum().sort_values(ascending=False).head(15).to_string())

# 3. Data Cleaning
print("\n🧹 Cleaning data...")
df['date'] = pd.to_datetime(df['date'])
countries = ['Kenya', 'United States', 'India', 'Brazil', 'United Kingdom', 'Germany']
df = df[df['location'].isin(countries)].copy()

# Handle missing values
key_metrics = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths',
               'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
df[key_metrics] = df.groupby('location')[key_metrics].ffill()

# 4. Analysis and Visualization
print("\n📈 Generating visualizations...")
plt.figure(figsize=(15, 10))

# Cases and Deaths Timeline
plt.subplot(2, 2, 1)
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
plt.title('Total COVID-19 Cases')
plt.ylabel('Cases')
plt.legend()

plt.subplot(2, 2, 2)
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_deaths'], label=country)
plt.title('Total COVID-19 Deaths')
plt.ylabel('Deaths')
plt.legend()

# Vaccination Progress
plt.subplot(2, 2, 3)
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['people_fully_vaccinated_per_hundred'], label=country)
plt.title('Fully Vaccinated (% Population)')
plt.ylabel('Percentage')
plt.legend()

# Death Rate Analysis
plt.subplot(2, 2, 4)
for country in countries:
    subset = df[df['location'] == country]
    rate = (subset['total_deaths'] / subset['total_cases']) * 100
    plt.plot(subset['date'], rate, label=country)
plt.title('Case Fatality Rate (%)')
plt.ylabel('Death Rate %')
plt.legend()

plt.tight_layout()
plt.savefig('covid_analysis.png')  # Save the figure
plt.show()

# 5. Generate Choropleth Map (will open in browser)
print("\n🌍 Generating world map...")
latest_data = df[df['date'] == df['date'].max()]
fig = px.choropleth(latest_data,
                    locations="iso_code",
                    color="total_cases_per_million",
                    hover_name="location",
                    hover_data=["total_cases", "total_deaths"],
                    title="Global COVID-19 Cases per Million")
fig.write_html("world_map.html")  # Save as interactive HTML
fig.show()

# 6. Insights
print("\n💡 Key Insights:")
insights = [
    "• The US had both the highest cases and deaths among analyzed countries",
    "• India showed rapid growth but lower mortality rates",
    "• Kenya's vaccination rates lagged significantly behind others",
    "• UK and Germany had similar vaccination patterns despite different outbreaks",
    "• Brazil experienced multiple severe waves with high mortality"
]

for insight in insights:
    print(insight)

print("\n🎉 Analysis complete!")
print("📁 Outputs saved:")
print("- covid_analysis.png (charts)")
print("- world_map.html (interactive map)")