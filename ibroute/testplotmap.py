#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 21:30:18 2019

@author: danw
"""

from geolayer import GeopyNominatimLayer
from waypointdata import get_waypoints_from_file, Categories
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader

wps = get_waypoints_from_file("../waypoints.txt")
api = GeopyNominatimLayer()

coded_wps = [api.get_geocoded_waypoint(_) for _ in wps]
#%%

plt.close("all")

data = {}
for cat in Categories:
    ##WTF why doesn't the enum comparison work??
    data[cat] = [_.latlong for _ in coded_wps if _.category.value == cat.value]

figsize = (14.4,7.2)
fig = plt.figure(figsize=figsize)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.background_patch.set_visible(False)



shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution="110m",
                                     category="cultural", name=shapename)

for state in shpreader.Reader(states_shp).geometries():
        # pick a default color for the land with a black outline,
        # this will change if the storm intersects with our track
        facecolor = [0.9375, 0.9375, 0.859375,0.2]
        edgecolor = 'black'
        ax.add_geometries([state], ccrs.PlateCarree(),
                          facecolor=facecolor, edgecolor=edgecolor)

for k,v in data.items():
    longs = [_[1] for _ in v]
    lats = [_[0] for _ in v]
    ax.scatter(longs,lats,color=str(k.value),
             transform = ccrs.PlateCarree())
    
for wpin, wpout in zip(wps, coded_wps):
    latlon = wpout.latlong
    ax.annotate(wpin.name, (latlon[1],latlon[0]))
    
plt.tight_layout()
    