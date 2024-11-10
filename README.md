# Shenzhen Urban Mobility Analysis 🏙️🚶📊

This project explores urban mobility patterns within Shenzhen, China, using OD (origin-destination) data and a spatial road network model. The analysis provides insights into travel trends, stay durations, and movement flows, supporting better urban planning and transportation decisions.

## Project Overview 🚀

This analysis focuses on understanding how people move through Shenzhen's urban areas. Key components include:

- **Road Network Visualization**: A detailed map of Shenzhen's road network, giving context to OD patterns.
- **Stay Duration Analysis**: Insights into the average time spent across different administrative zones, revealing popular areas and temporal activity patterns.
- **OD Travel Analysis by Time Period**: Visualization of OD travel flows across four daily time periods, highlighting peak times and routes between regions.

The project combines data visualization, spatial analysis, and statistical processing to create a comprehensive view of mobility in Shenzhen.

## Key Contributions 🎉

1. **Enhanced Urban Insight**: Provides an in-depth look into how and when people move, aiding city planners in identifying high-traffic zones and peak travel times.
2. **Road Network Visualization**: Uses `osmnx` and `networkx` to model and visualize Shenzhen's road network, offering a foundation for detailed mobility analysis.
3. **Time-Based OD Analysis**: Breaking down OD patterns by time periods allows stakeholders to pinpoint rush hours and assess varying regional traffic flows.
4. **Stay Duration Distribution**: Analyzes stay durations by district, which can help optimize services and resources for specific areas of Shenzhen.

## Visual Results 📈

### 1. Road Network Visualization 🛣️
A clear visualization of Shenzhen's road network, providing a foundational map for the OD analysis.

![Road Network](./out/pic/roadnet_shenzhen.svg)

### 2. Stay Duration Analysis ⏳
Box plots illustrating the average stay duration in each region. This helps identify areas with longer stays, potentially indicating high-interest zones.

![Stay Duration](./out/pic/boxplot_of_stay_time_by_county.svg)

### 3. OD Travel Analysis by Time Period 🕒
OD distributions displayed across four daily time slots: early morning, mid-morning, afternoon, and evening. Below is an example for the 6-10h period, showing popular routes and movement patterns.

![OD Pattern](./out/pic/od_county_2_uv_6_10h.svg)

## How to Use 🧑‍💻

1. **Environment Setup**:
   Install required packages to ensure smooth running:
   
   ```shell
   pip install numpy pandas geopandas matplotlib osmnx networkx sklearn shapely
