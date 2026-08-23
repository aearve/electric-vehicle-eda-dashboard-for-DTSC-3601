WASHINGTON STATE ELECTRIC VEHICLE POPULATION EDA
==================================================

Author: Arnav Earve
Course: DTSC 3601

PROJECT DESCRIPTION
--------------------
This project is an interactive Streamlit dashboard exploring the Washington 
State Department of Licensing's Electric Vehicle Population Data. The dataset 
contains registration records for every Battery Electric Vehicle (BEV) and 
Plug-in Hybrid Electric Vehicle (PHEV) registered in the state, including 
make, model, model year, electric range, county/city, and more.

DATASET
--------------------
Source: Kaggle - "Electric Vehicle Population Data"
File: Electric_Vehicle_Population_Data.csv
Rows: 177,866
Columns: 17

HOW TO RUN
--------------------
1. Install dependencies with uv:
   uv add streamlit pandas matplotlib seaborn

2. Run the app:
   uv run streamlit run app.py

3. Open the local URL shown in the terminal (e.g. http://localhost:8501) 
   in your browser.

FEATURES
--------------------
- Sidebar filters by County and Make
- Overview tab with key metrics (total vehicles, unique makes, average 
  electric range, top county, percent battery electric)
- EDA tab with a data sample, dataset shape, column data types, and 
  missing value counts
- Visualizations tab with charts including: top 10 vehicle makes, electric 
  vehicle type distribution, electric range distribution, vehicles 
  registered by model year, and top counties by EV count

SCREENSHOTS
--------------------
See the /screenshots folder in this repository for images of the running 
application:
- screenshots/overview.png       - Overview tab with key metrics
- screenshots/eda.png            - EDA tab with data sample and statistics
- screenshots/visualizations.png - Visualizations tab with charts

TECH STACK
--------------------
Python, Streamlit, pandas, matplotlib, seaborn, uv (package manager)
