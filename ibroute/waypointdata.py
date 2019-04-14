#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 21:05:30 2019

@author: danw
"""

from collections import namedtuple
from typing import List
import us
from enum import Enum

class Categories(Enum):
    GREEN = "green"
    ORANGE = "orange"
    YELLOW = "yellow"
    BLUE = "blue"
    PINK = "pink"


waypoint_in = namedtuple("waypoint_in", ["id", "name", "category", "state"])

def parse_text_line_to_waypoint(text: str) -> waypoint_in:
    tokens = [_.strip() for _ in text.split(",")]
    wpid = int(tokens[0])
    name  = tokens[1].strip()
    cat = Categories(tokens[2])
    state = us.states.lookup(tokens[3])
    return waypoint_in(wpid, name, cat, state)


def get_waypoints_from_file(path: str) -> List[waypoint_in]:
    wps = []
    with open(path,"r") as f:
        for line in f:
            if line.startswith("#"):
                               continue
            wps.append(parse_text_line_to_waypoint(line))
    return wps


