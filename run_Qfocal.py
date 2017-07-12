# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 12:44:01 2016

@author: obrien
"""
import Qfocal

#--- set paths ---#
infile = r"./GeoNet_CMT_solutions.csv"
path_to_beachballs = r"./beachballs"
path_to_shp = r"./cmt/"

#--- make dirs, if they exist they will be removed and re-made ---#
Qfocal.make_dir(path_to_beachballs)
Qfocal.make_dir(path_to_shp)

#--- load cmt file ---#
data = Qfocal.np_load_GeoNet_centroid_data(infile)

#--- do stuff ---#
x = data['lon']
y = data['lat']
fm = []
fm = zip(data['str1'], data['dip1'], data['rake1'])   
path_to_beachballs = Qfocal.make_beachballs(data, path_to_beachballs,
                                            fm, fmt='.svg')
Qfocal.make_shapefile(data, path_to_shp, path_to_beachballs)