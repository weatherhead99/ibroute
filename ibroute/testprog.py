#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 22:23:54 2019

@author: danw
"""

import pickle
from os.path import exists

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from ibroute.geolayer import GeopyNominatimLayer
from ibroute.waypointdata import get_waypoints_from_file, Categories
from ibroute.routing import CachedDistanceMatrix


CACHE_FILE_NAME = "../distance_matrix_cache.pickle"

api = GeopyNominatimLayer()

if exists(CACHE_FILE_NAME):
    print("reloading waypoints from cache")
    cdm = CachedDistanceMatrix.load_from_file(CACHE_FILE_NAME, api)
else:
    print("loading waypoints from input file")
    wps = get_waypoints_from_file("../waypoints.txt")
    coded_wps = [api.get_geocoded_waypoint(_) for _ in wps]    
    home = coded_wps[0] #joshua tree for now
    cdm = CachedDistanceMatrix(api, coded_wps, home)
    print("caching distance matrix...")
    cdm.save_to_file(CACHE_FILE_NAME)


manager = pywrapcp.RoutingIndexManager(len(cdm), 1, cdm.home.id)
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
#    print("from idx: %d, to_index: %d" % (from_index, to_index))
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
#    print("from_node: %d, to_node: %d" % (from_node,to_node))
    dist = int(round(cdm.distance_matrix_element(from_node,to_node)))
#    print("distance: %d" % dist)
    return dist

def print_solution(manager, routing, assignment):
    """Prints assignment on console."""
    print('Objective: {} miles'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def get_solution_sequence(manager, routing, assignment):
    index = routing.Start(0)
    route_distance = 0
    plan = []
    while not routing.IsEnd(index):
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan.append(manager.IndexToNode(index))
    return plan


transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

    # Solve the problem.
print("calculating solution")
assignment = routing.SolveWithParameters(search_parameters)

if(assignment):
    print_solution(manager,routing,assignment)
    solnplan = get_solution_sequence(manager, routing, assignment)
    with open("../solution.pickle", "wb") as f:
        pickle.dump({"solnplan": solnplan}, f)
