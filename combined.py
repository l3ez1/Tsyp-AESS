import pandas as pd

# Load the processed data and forecast data
df_processed = pd.read_csv("processed_land_cover_data.csv")  # Historical data (2001-2023)
df_forecast = pd.read_csv("all_forecasted_land_cover.csv")  # Forecast data (2024-2033)

# Melt the processed data for easier merging
df_processed_melted = df_processed.melt(id_vars=["Year"], var_name="Land_Cover_Type", value_name="Value")

# Rename the columns of forecast data for merging
df_forecast.rename(columns={"ds": "Year", "yhat": "Value"}, inplace=True)

# Combine the historical and forecast data
df_combined = pd.concat([df_processed_melted, df_forecast[["Year", "Value", "Land_Cover_Type"]]])

# Save the combined data to a CSV file
df_combined.to_csv("combined_land_cover_data.csv", index=False)

# Check the combined data
print("Combined data saved to 'combined_land_cover_data.csv'.")
print("Combined Data Preview:")
print(df_combined.head())
