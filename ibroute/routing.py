#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 22:11:19 2019

@author: danw
"""

from typing import Sequence
from ibroute.geolayer import waypoint_geocoded, GeoLayer
from collections import OrderedDict
from warnings import warn
from pickle import load, dump


class CachedDistanceMatrix:
    CACHE_SIZE = 2000
    def __init__(self,geolayer: GeoLayer, 
                 waypoints: Sequence[waypoint_geocoded]):
        self._geolayer = GeoLayer
        self._waypointmap = {_.id : _ for _ in waypoints}
        self._distance_matrix_cache = OrderedDict()
    
    def distance_matrix_element(self, i: int, j: int) -> float:
        fromto = (min(i,j),max(i,j))
        if fromto in self._distance_matrix_cache:
            return self._distance_matrix_cache[fromto]
        elif len(self._distance_matrix_cache) >= self.CACHE_SIZE:
            warn("cache is full, dropping old items")
            self._distance_matrix_cache.popitem(last=False)
        fromlatlong = self._waypointmap[i].latlong
        tolatlong = self._waypointmap[j].latlong
        distance = self._geolayer.get_distance_miles(fromlatlong, tolatlong)
        self._distance_matrix_cache[fromto] = distance
        return distance

    def save_to_file(self, fname: str) -> None:
        dct = {"waypointmap" : self._waypointmap,
               "distance_matrix_cache" : self._distance_matrix_cache}
        with open(fname, "wb") as f:
            dump(dct,f)

    @classmethod
    def load_from_file(cls, fname: str, geolayer: GeoLayer):
        with open(fname,"rb") as f:
            data = load(f)
            
        thisinstance = cls.__new__(cls)
        thisinstance._geolayer = geolayer
        thisinstance._waypointmap = data["waypointmap"]
        thisinstance._distance_matrix_cache = data["distance_matrix_cache"]
        
        return thisinstance
        
        
        
        
        
    
    
    