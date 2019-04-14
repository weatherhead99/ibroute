#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 21:17:16 2019

@author: danw
"""

from waypointdata import waypoint_in
from abc import abstractmethod
from typing import Tuple
from collections import namedtuple

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

waypoint_geocoded = namedtuple("waypoint_geocoded",["id", "latlong", 
                                                    "category", "state"])

LatLongT = Tuple[float,float]

class GeoLayer:
    @abstractmethod
    def get_lattitude_longitude(self, placename: str) -> LatLongT:
        pass
        
    @abstractmethod
    def get_distance_miles(self, ll1: LatLongT, ll2: LatLongT) -> float:
        pass
    
    def get_geocoded_waypoint(self, wpin: waypoint_in) -> waypoint_geocoded:
        latlong = self.get_lattitude_longitude("%s, %s, USA" % 
                                               (wpin.name,wpin.state.abbr))
        
        wpout = waypoint_geocoded(id=wpin.id, latlong=latlong,
                                  category=wpin.category, state=wpin.state)
        return wpout


class GeopyNominatimLayer(GeoLayer):
    def __init__(self):
        self._api = Nominatim(user_agent="ibroute/0.1")

    def get_lattitude_longitude(self, placename: str) -> LatLongT:
        location = self._api.geocode(placename)
        if location is None:
            raise ValueError("couldn't geocode place: %s" % placename)
        return (location.latitude, location.longitude)

    def get_distance_miles(self, ll1: LatLongT, ll2: LatLongT) -> float:
        dist = geodesic(ll1,ll2)
        return dist.miles