# NYC Crime Analytics

This project analyzes and visualizes crime data from the New York City Police Department. It fetches crime data using the NYC Open Data API and generates an interactive map that displays crime locations across New York City. The map includes markers for individual crime incidents and heatmaps for different crime types. Additionally, the time range of the data is displayed on the map.

## Features
- Fetches crime data from the NYC Open Data API (`5uac-w243` dataset).
- Processes the data with pandas, cleaning date columns and handling missing values.
- Visualizes crime data using the Folium library, with markers and heatmaps for various crime types.
- Includes a time range of the data on the map.
- Saves the map as an HTML file for easy viewing in any web browser.

## Requirements
Before running the script, make sure you have the following Python packages installed:

- `pandas`
- `folium`
- `sodapy`
- `dotenv`
- `requests`

You can install these dependencies using pip:

```bash
pip install pandas folium sodapy python-dotenv requests
```

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/ericmaddox/nyc-crime-analytics.git
   cd nyc-crime-analytics
   ```

2. Create a `.env` file in the root directory of the project to store your Socrata API token:

   ```bash
   touch .env
   ```

3. Add your API token to the `.env` file:

   ```
   API_TOKEN=your_socrata_api_token_here
   ```

   You can obtain an API token by signing up at [NYC Open Data](https://opendata.cityofnewyork.us/).

## Usage

Once your environment is set up, you can run the `nyc_crime_analytics.py` script:

```bash
python nyc_crime_analytics.py
```

This will fetch crime data, process it, and generate an interactive HTML map. The map will be saved to a file named `nyc_crime_analysis_map.html` in the project directory. You can open this file in any web browser to view the crime data visualization.

## File Description

- `nyc_crime_analytics.py`: Main Python script that fetches and processes the crime data and generates the interactive map.
- `.env`: Environment file for storing the Socrata API token securely.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, create a new branch, and submit a pull request. Please ensure that your code adheres to the coding standards and includes tests where applicable.

## Acknowledgments

- NYC Open Data API for providing the crime data.
- Socrata API for enabling access to city datasets.
- Folium for mapping and visualization.
