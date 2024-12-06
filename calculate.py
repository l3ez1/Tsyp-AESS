import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

# Load the actual data
actual_data = pd.read_csv('processed_land_cover_data.csv')

# Load the forecasted data (all_forecasted_land_cover.csv)
forecast_data = pd.read_csv('all_forecasted_land_cover.csv')

# Make sure the 'Year' column in both dataframes is of type int
actual_data["Year"] = actual_data["Year"].astype(int)

# Filter forecast data to match the actual years (2001-2023)
forecast_data['Year'] = pd.to_datetime(forecast_data['ds']).dt.year
forecast_data = forecast_data[forecast_data['Year'].between(2001, 2023)]

# Debugging: Check if the year range and Land_Cover_Type are matching
print("Actual Data Years: ", actual_data['Year'].unique())
print("Forecast Data Years: ", forecast_data['Year'].unique())

# Prepare a list to hold the RMSE results for each land cover type
rmse_results = []

# Calculate RMSE for each land cover type
for column in actual_data.columns[1:]:
    print(f"Processing Land Cover Type: {column}")
    
    # Merge actual and forecasted data by Year and Land_Cover_Type
    merged_data = pd.merge(actual_data[['Year', column]], forecast_data[['Year', 'Land_Cover_Type', 'yhat']], 
                           on='Year', how='inner')
    
    print(f"Merged Data for {column}:")
    print(merged_data.head())  # Display the first few rows of merged data
    
    # Filter data by land cover type
    merged_data = merged_data[merged_data['Land_Cover_Type'] == column]
    
    if not merged_data.empty:
        # Calculate RMSE
        rmse = np.sqrt(mean_squared_error(merged_data[column], merged_data['yhat']))
        rmse_results.append({'Land_Cover_Type': column, 'RMSE': rmse})
    else:
        print(f"No matching data found for {column}. Skipping...")
        
# Convert RMSE results into a DataFrame
rmse_df = pd.DataFrame(rmse_results)

# Save the RMSE results to a CSV
rmse_df.to_csv('rmse_results.csv', index=False)

# Display the RMSE results
print(rmse_df)
