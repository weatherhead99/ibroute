#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 22:42:35 2019

@author: danw
"""

from ibroute.routing import CachedDistanceMatrix
from pkg_resources import resource_filename

waypoints_file = resource_filename("ibroute", "waypoints.txt")
