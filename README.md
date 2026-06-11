# Danube Water Level Monitor

A robust Python-based tool to monitor real-time water levels on the Danube River (Budapest station). This script fetches data directly from the official [hydroinfo.hu](https://www.hydroinfo.hu/) portal, providing an automated way to track water levels, discharge, and temperature.

## Features
- **Real-time Monitoring:** Tracks water levels, discharge, and temperature.
- **Accurate Timestamping:** Correctly parses the observation time which is hidden in nested `iframe` structures on the website.
- **Reliable Connectivity:** Employs browser-like User-Agent headers to ensure the script is not blocked by the server's anti-bot mechanisms.
- **Lightweight & Efficient:** Uses `BeautifulSoup` for high-performance HTML parsing.

## How it works
The `hydroinfo.hu` portal uses a complex frameset structure. This script bypasses the main container and connects directly to the sub-pages containing the raw data:
1. **Timestamp source:** `tables/dunhid_f.html` – This contains the official "Observation" (Észlelés) timestamp.
2. **Data source:** `tables/dunhif_a.html` – This contains the structured hydrological table.

The script combines these two data points to provide you with the most up-to-date and context-aware information.

## Prerequisites
You need [Python](https://www.python.org/) installed. Install the necessary libraries via terminal:

```bash
pip install requests beautifulsoup4


How to use
1 Save the code as duna_monitor.py.

2 Run it from your terminal: python duna_monitor.py

3 The script will automatically fetch and display the data
  every 60 seconds.
  
  Useful Information & Troubleshooting
  
  Why did we choose these URLs? The main page (duna.html) is just a visual container. The raw data resides in the tables/ directory,
  which is much faster and more reliable to scrape.
  
  Updating Interval: The script is set to update every 60 seconds.
  You can modify the time.sleep(60) line to a higher number
  (e.g., 3600 for 1 hour) if you want to update less frequently.
  
  Server Timeouts: If you experience connection issues,
  the script includes a 10-second timeout to ensure the program
  doesn't hang.
  
  Maintenance: If the data stops appearing (e.g., "Data not found"),
  it means the website's HTML structure has changed.
  Simply re-examine the target URLs using browser developer tools (F12)
  to see if the structure has moved.
  
  
  
  
  
