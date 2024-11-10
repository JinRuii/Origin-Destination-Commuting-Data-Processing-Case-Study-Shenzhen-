# Shenzhen Urban Mobility Analysis 🏙️🚶📊

This project explores urban mobility patterns within Shenzhen, China, with a focus on urban villages and their role in city dynamics. Using origin-destination (OD) data and a spatial road network model, this analysis provides insights into travel trends, stay durations, and movement flows, supporting better urban planning and transportation decisions.

This project is inspired by the methodologies and findings presented in the article "Destigmatizing urban villages by examining their attractiveness: Quantification evidence from Shenzhen" published in Habitat International.
https://doi.org/10.1016/j.habitatint.2024.103120

## Project Overview 🚀

This analysis focuses on understanding how people move through Shenzhen's urban areas, particularly examining urban villages. Key components include:

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

### 1. OD Travel Analysis by Time Period 🕒
![image](https://github.com/user-attachments/assets/b2b1cc69-034e-4a24-b634-e8dc4694e27b)


## How to Use 🧑‍💻

1. **Environment Setup**:
   Install required packages to ensure smooth running:
   
   ```shell
   pip install numpy pandas geopandas matplotlib osmnx networkx sklearn shapely
