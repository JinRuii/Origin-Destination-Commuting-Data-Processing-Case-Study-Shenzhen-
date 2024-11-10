# Import required libraries
import warnings

warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import osmnx as ox
import networkx as nx
import pickle
from sklearn.cluster import KMeans
from shapely.geometry import LineString

# Global plot configuration
plt.rcParams['font.sans-serif'] = ['Heiti TC']

# 1. Data Loading
# Load urban village and full grid data
grid_uv = gp.read_file('./data/fnid_shenzhen.shp')
grid_sz = gp.read_file('./data/urbanvillage_fnid.shp')
trace = pd.read_csv('./data/OD data_Shenzhen_500.csv', index_col=0)
county_guangming = gp.read_file('./data/PSI/guangming.shp')

# Load road network data
with open('./out/map_graph.pkl', 'rb') as f:
    streets_graph = pickle.load(f)

# Convert road network to GeoDataFrame format for spatial analysis
streets = ox.graph_to_gdfs(ox.get_undirected(streets_graph), nodes=False, edges=True, node_geometry=False,
                           fill_edge_geometry=True)

# 2. Plot Shenzhen Road Network
f, ax = plt.subplots(figsize=(10, 6))
streets.plot(ax=ax, linewidth=0.2)
ax.set_axis_off()
ax.set_xlim(113.75, 114.7)
ax.set_ylim(22.45, 22.9)
plt.savefig('./out/pic/roadnet_shenzhen.svg')
plt.show()

# 3. Data Preprocessing
# Convert the coordinate system of Guangming county, perform spatial matching, and associate it with Shenzhen region
county_guangming.to_crs('epsg:4326', inplace=True)
temp = gp.sjoin(grid_sz[['fnid', 'county_nam', 'geometry']], county_guangming[['ENG_NAME', 'geometry']],
                op='intersects', how='left')
guangming_idx = (temp['ENG_NAME'] == 'Guangming') & (temp['county_nam'] == '宝安区')

# Map administrative regions to English names
eng_name_dict = {'南山区': 'Nanshan', '罗湖区': 'Luohu', '福田区': 'Futian', '宝安区': 'Baoan',
                 '龙岗区': 'Longgang', '盐田区': 'Yantian', '龙华区': 'Longhua', '坪山区': 'Pingshan',
                 '大鹏新区': 'Dapeng'}
grid_sz['county_name'] = grid_sz['county_nam'].apply(lambda x: eng_name_dict[x])
grid_sz.loc[guangming_idx, 'county_name'] = temp.loc[guangming_idx, 'ENG_NAME']

# Calculate the centroid coordinates of each grid cell
grid_sz[['grid_lng', 'grid_lat']] = grid_sz['geometry'].apply(lambda x: pd.Series(x.centroid.coords[0]))

# Aggregate grids by administrative region and generate the centroid
county_sz = grid_sz.groupby(['county_cod', 'county_name']).apply(lambda x: x.unary_union).reset_index()
county_sz.rename(columns={0: 'geometry'}, inplace=True)
county_sz = gp.GeoDataFrame(county_sz)
county_sz[['cent_lng', 'cent_lat']] = county_sz['geometry'].apply(lambda x: pd.Series(x.centroid.coords[0]))


# 4. Data Expansion
# Since `trace_valid` includes the number of people, we expand each row based on the count to facilitate more granular analysis
def data_inflation(fnid, d_county, stay_seconds, cnt):
    for _ in range(cnt):
        trace_stay.append([fnid, d_county, stay_seconds])


trace_stay = []
_ = list(map(lambda x: data_inflation(x[0], x[1], x[2], x[3]),
             trace_valid[['fnid', 'd_county', 'stay_seconds', 'cnt']].values.tolist()))
df_trace_stay = pd.DataFrame(trace_stay, columns=['d_fnid', 'd_county', 'stay_seconds'])
df_trace_stay['stay_hour'] = (df_trace_stay['stay_seconds'] / 3600).round(2)

# Descriptive statistics of average stay time by region
trace_stay_des = df_trace_stay.groupby('d_county').apply(lambda x: x['stay_hour'].describe())
display(trace_stay_des)

# 5. Boxplot of Stay Duration Distribution by Administrative Regions
fig, ax = plt.subplots(figsize=(8, 6))
df_trace_stay.boxplot(column='stay_hour', by='d_county', ax=ax, rot=0, grid=True)
ax.set_title('Stay Duration Distribution by Administrative Region')
ax.set_xlabel('Destination County')
ax.set_ylabel("Stay Time (hours)")
plt.savefig('./out/pic/boxplot_of_stay_time_by_county.svg')
plt.show()


# 6. Define OD Travel Analysis Plotting Function
def plot_od(od_list, v_max, county_color, title_name=None, max_od_line_width=5, fig_save_path=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title_name)
    m = Basemap(llcrnrlon=113.7, llcrnrlat=22.4, urcrnrlon=114.7, urcrnrlat=22.9, resolution='l', projection='cyl',
                ax=ax)
    m.drawmeridians(np.arange(113, 115, 0.2), linewidth=0.5, fontsize=10, labels=[0, 0, 0, 1], color='silver')
    m.drawparallels(np.arange(22, 23, 0.2), rotation=90, linewidth=0.5, fontsize=10, labels=[1, 0, 0, 0],
                    color='silver')
    county_sz['geometry'].boundary.plot(ax=ax, alpha=0.5, color='grey', linewidth=1, zorder=1)

    # Normalization tool to map OD data values to [0, 1] interval
    norm = matplotlib.colors.Normalize(vmin=0, vmax=v_max)

    # Draw OD lines
    for x in od_list:
        color_x = county_color[x[0]]
        linewidth_x = norm(x[1]) * max_od_line_width
        ax.plot([x[2], x[4]], [x[3], x[5]], color=color_x, linewidth=linewidth_x, alpha=0.5)

    if fig_save_path:
        plt.savefig(fig_save_path)
    plt.show()


# 7. OD Travel Analysis by Time Period and Plotting
# For each time period (0-6h, 6-10h, 10-16h, 16-24h), calculate and plot OD travel data
for time_period, label in zip(['0_6h', '6_10h', '10_16h', '16_24h'], ['0-6h', '6-10h', '10-16h', '16-24h']):
    v_max = county_uv_od[f'county_2_uv_{time_period}'].max()
    od_list = county_uv_od[county_uv_od[f'county_2_uv_{time_period}'] > 0][
        ['o_county', f'county_2_uv_{time_period}', 'o_lng', 'o_lat', 'd_lng', 'd_lat']].values.tolist()
    plot_od(od_list, v_max, county_color, title_name=f'OD Distribution {label}', max_od_line_width=5,
            fig_save_path=f'./out/pic/od_county_2_uv_{time_period}.svg')
