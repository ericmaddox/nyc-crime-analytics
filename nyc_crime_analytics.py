import pandas as pd
from sodapy import Socrata
import folium
from folium import FeatureGroup, LayerControl, Map
from folium.plugins import HeatMap
from folium.features import DivIcon
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the credentials from environment variables
API_TOKEN = os.getenv('API_TOKEN')

# Initialize the Socrata API client with the API token
client = Socrata(
    "data.cityofnewyork.us", 
    API_TOKEN
)

# Fetch data from the NYC crime dataset
results = client.get("5uac-w243", limit=50000)  # Increase the limit to fetch more records

# Convert the results to a pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# Print the available columns and the first few rows of the data to understand its structure
print("Columns in the DataFrame:", results_df.columns)
print("First few rows of the data:", results_df.head())

# Convert date columns to datetime
results_df['cmplnt_fr_dt'] = pd.to_datetime(results_df['cmplnt_fr_dt'], errors='coerce')
results_df['cmplnt_to_dt'] = pd.to_datetime(results_df['cmplnt_to_dt'], errors='coerce')

# Drop rows with NaT (Not a Time) values in the date columns
results_df = results_df.dropna(subset=['cmplnt_fr_dt', 'cmplnt_to_dt'])

# Find the earliest and latest dates in the dataset
start_date = results_df['cmplnt_fr_dt'].min()
end_date = results_df['cmplnt_to_dt'].max()

# Initialize the base map centered on New York City with an appropriate zoom level
crime_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)  # Adjust the zoom level as needed

# Dictionary to hold crime type layers and heatmaps data
crime_layers = {}
crime_heatmaps = {}

# Populate crime_layers and crime_heatmaps for each unique crime type
unique_crime_types = results_df['ofns_desc'].unique()
for crime_type in unique_crime_types:
    crime_layers[crime_type] = FeatureGroup(name=crime_type, show=False)
    crime_heatmaps[crime_type] = []

# Loop through the rows and add markers for each crime record
for idx, row in results_df.iterrows():
    try:
        if pd.isna(row['latitude']) or pd.isna(row['longitude']):
            continue

        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        crime_type = row.get('ofns_desc', 'Unknown')
        precinct = row.get('addr_pct_cd', 'Unknown')
        boro = row.get('boro_nm', 'Unknown')
        date = row.get('cmplnt_fr_dt', 'Unknown')

        # Create a popup with crime data
        popup = folium.Popup(f"<b>Crime Type:</b> {crime_type}<br><b>Precinct:</b> {precinct}<br><b>Borough:</b> {boro}<br><b>Date:</b> {date}", max_width=300)

        # Add marker to respective layer based on crime type
        marker = folium.Marker(location=[latitude, longitude], popup=popup, icon=folium.Icon(color='blue', icon='info-sign'))
        crime_layers[crime_type].add_child(marker)
        crime_heatmaps[crime_type].append([latitude, longitude])

    except Exception as e:
        print(f"Error processing row {idx}: {e}")

# Add layers and heatmaps to the map
for crime_type, layer in crime_layers.items():
    layer.add_to(crime_map)
    HeatMap(crime_heatmaps[crime_type], name=f"{crime_type} Heatmap", radius=25, blur=15, max_zoom=17, show=False).add_to(crime_map)

# Add layer control to the map
LayerControl(collapsed=False).add_to(crime_map)

# Add time range to the map as a caption
caption_html = f"""
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 300px; height: 90px; 
            background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
            ">&nbsp; Time Range of Data: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}
</div>
"""
crime_map.get_root().html.add_child(folium.Element(caption_html))

# Save the updated map to an HTML file
crime_map.save("nyc_crime_analysis_map.html")
print("Map with crime data has been saved to 'nyc_crime_analysis_map.html'. You can open it in your browser.")
