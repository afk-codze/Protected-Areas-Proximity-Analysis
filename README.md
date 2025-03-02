# Natura 2000 Proximity Analysis

## Overview

This project is an automation script that analyzes the proximity of given addresses to protected areas in the Natura 2000 network using geospatial data. The script:

- Geocodes addresses using the Google Geocoding API.
- Loads Natura 2000 protected area data from an external source.
- Converts and buffers the locations.
- Checks if addresses fall within a 1 km radius of Natura 2000 areas.
- Outputs results to a CSV file.

## Project Structure

```
├── Natura2000_end2021_rev1_gpkg/   # Folder (empty, dataset must be downloaded separately)
├── addresses.json                  # JSON file with addresses to analyze
├── geolocal.py                      # Main Python script
├── proximity_results.csv            # CSV output with proximity analysis results
```

## Requirements

- Python 3.x
- Google API Key (stored in a `.env` file)
- Required Python libraries:
  - `geopandas`
  - `shapely`
  - `pandas`
  - `requests`
  - `dotenv`
  - `logging`

## Installation

1. Clone the repository:

   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:

   ```sh
   pip install geopandas shapely pandas requests python-dotenv
   ```

3. Create a `.env` file in the root directory and add your Google API Key:

   ```sh
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Ensure `addresses.json` contains the addresses to analyze in the following format:

   ```json
   [
       {"id": 1, "address": "Via Roma, 1, 80045 Pompei NA"},
       {"id": 2, "address": "Piazza del Duomo, 12, 50122 Firenze FI"},
       {"id": 3, "address": "Via San Giovanni Bosco, 5, 75100 Matera MT"},
       {"id": 4, "address": "Via delle Vigne, 19, 00074 Nemi RM"},
       {"id": 5, "address": "Corso Umberto I, 22, 07041 Alghero SS"}
   ]
   ```

2. Run the script:

   ```sh
   python geolocal.py
   ```

3. The results will be saved in `proximity_results.csv`:

   ```csv
   id,latitude,longitude,near_protected_area
   1,41.9028,12.4964,True
   2,48.8566,2.3522,False
   ```

## Notes

- Ensure your Google API Key has Geocoding API enabled.
- The Natura 2000 dataset is not included in this repository due to size limitations but can be downloaded from official sources at [Natura 2000 Network](https://www.eea.europa.eu/data-and-maps/data/natura-11).

## Disclaimer

The Natura 2000 dataset used in this project is sourced from official environmental and governmental agencies. This project is for informational and analytical purposes only. Users are responsible for ensuring compliance with data usage policies and verifying results before applying them in decision-making processes.
