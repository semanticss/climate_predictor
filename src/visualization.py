import cartopy
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import geopandas as gpd
import os
import json

# loading json
with open("../src/county_disaster_counts_by_year.json", "r") as f:
    disaster_data = json.load(f)


records = []
for geoid, data in disaster_data.items():
    total = sum(data["disasters_by_year"].values())
    record = {
        "GEOID": geoid,
        "county_name": data["county_name"],
        "total_disasters": total
    }
    records.append(record)

    disaster_df = pd.DataFrame(records)


shapefile_path = '../data/raw/tl_2024_us_county/tl_2024_us_county.shp'
counties = gpd.read_file(shapefile_path)
counties = counties.to_crs(epsg=4326) # idk what this even means but everything breaks without it
countries_GEOID = counties['GEOID']

counties = counties.merge(disaster_df, on="GEOID", how="left")


fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={"projection": ccrs.PlateCarree()})
counties.plot(column="total_disasters", cmap="Reds", linewidth=0.1, edgecolor="black", ax=ax, legend=True)

ax.set_extent([-125, -66.5, 24, 50], crs=ccrs.PlateCarree())
ax.add_feature(cartopy.feature.STATES, edgecolor="gray", linewidth=0.5)
ax.set_title("Total Disaster Declarations per County", fontsize=16)

plt.savefig("us_disaster_map.png", dpi=150, bbox_inches='tight')
plt.show()