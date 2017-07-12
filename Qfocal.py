# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 12:39:08 2016

@author: obrien

functions for QGIS_focal
"""
import numpy as np
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import shutil
import shapefile
from from_obspy import beachball


def make_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    else:
        shutil.rmtree(dirpath)
        os.mkdir(dirpath)


def makedate(text):
    return datetime.datetime.strptime(text, '%Y%m%d%H%M%S')
       
       
def np_load_GeoNet_centroid_data(filename):
    """
    Open the downloaded GeoNet_CMT_solutions.csv
    """
    data = np.genfromtxt(filename,
                         delimiter=',', skip_header=1, skip_footer=8,
                         names=True,
                         dtype=['|S12','object','float','float','float','float',
                               'float','float','float','float','float','float',
                               'float','float','float','float','float','float',
                               'float','float','float','float','float','float',
                               'float','float','float','float','float','float',
                               'float','float'],
                         converters={1: makedate})    
    return data
    
            
def getWKT_PRJ(epsg_code):# 4326
    import urllib
    wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    remove_spaces = wkt.read().replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output
 

def make_shapefile(data, path, ptb=None):
    shp_writer = shapefile.Writer(shapefile.POINT)
    shp_writer.autoBalance = 1
    shp_writer.field('Event_ID', 'C', 50)
    shp_writer.field('Date', 'C', 50)
    shp_writer.field('Longitude', 'C', 50)
    shp_writer.field('Latitude', 'C', 50)
    shp_writer.field('CD', 'C', 50)
    shp_writer.field('MW', 'C', 50)
    shp_writer.field('T_axis_pl', 'C', 50)
    shp_writer.field('T_axis_az', 'C', 50)
    shp_writer.field('P_axis_pl', 'C', 50)
    shp_writer.field('P_axis_az', 'C', 50)
    shp_writer.field('Focal_mech', 'C', 100)
    for i, eq in enumerate(data):
        shp_writer.point(eq['lon'], eq['lat'])
        shp_writer.record(eq['event_id'], eq['datetime'].isoformat(),
                          eq['lon'], eq['lat'], eq['CD'], eq['mw'],
                          eq['tpl'], eq['taz'], eq['ppl'], eq['paz'], ptb[i])        
    shp_writer.save(path+"CMT_on_hik")
    # create a projection file
    prj = open(path+"CMT.prj", "w")
    epsg = getWKT_PRJ("4326")
    prj.write(epsg)
    prj.close()


def color_by_depth_equal(depth, x):
    norm = mpl.colors.Normalize(depth.min(), depth.max())
    cmap = plt.cm.jet_r
    m = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    return m.to_rgba(x)


def make_beachballs(data, path, fm, fmt='.svg'):
    path_to_beachballs = path
    saved_beachballs = []
    for i in range(len(fm)):
        eqname = str('eq_'+data['event_id'][i])
        savebeach = os.path.join(path_to_beachballs, eqname+fmt)
        width = (data['mw'][i]*100)#/2
        beachball.Beachball(fm[i], xy=(data['lon'][i], data['lat'][i]),
                            width=width,
                  facecolor=color_by_depth_equal(data['CD'], data['CD'][i]),
                  linewidth=1, outfile=savebeach)        
        saved_beachballs.append(savebeach)
        plt.close()
    return saved_beachballs
