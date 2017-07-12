# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:39:26 2016

@author: obrien
"""

# this script will draw beachballs and create the kml file 
# can be readily plotted in googleearth. 
# All created elements are placed in the same directory
# The kml file and the beachballs have to stay in the same directory, until it is a kmz. 

from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import numpy as np
import datetime as date
import sys
import Qfocal
import matplotlib.pyplot as plt
from obspy.imaging.beachball import Beachball

infile = r"./GeoNet_CMT_solutions.csv"
beachout = r"./beachballs/"
kmlout = r"./beachballs/Focal_mechanism_devy.kml"

Qfocal.make_dir(beachout)

data = Qfocal.np_load_GeoNet_centroid_data(infile)
#--- Arcgis doesn't cope well with more than 1000 image files at once ---#
data = data[0:50] # take a sample

def beachball(data):
    """function to draw beachball, slightly different from Qfocal"""
    strike, dip, rake = data['str1'],data['dip1'],data['rake1']
    #event = np.arange(0, len(data),1)
    for j in range(len(strike)):
        width = (data['mw'][j]*100)#/2
        fm_SDR = [strike[j], dip[j], rake[j]]
        #fm_NM = [data['mxx'][j], data['mxy'][j], data['mxz'][j],
        #         data['myy'][j], data['myz'][j], data['mzz'][j]]
        Beachball(fm_SDR, outfile=beachout+str(data['event_id'][j]),
                  facecolor=Qfocal.color_by_depth_interval(data['CD'][j]),
                  width=width,
                  edgecolor='black')
        plt.close() 

beachball(data)

latitude = data['lat']
longitude = data['lon']
event_id = data['event_id']
index = np.arange(0, len(data),1)
dt = data['datetime']

yyyy, mm, dd, hr, mn, ss = [], [], [], [], [], []
for i, d in enumerate(dt):
    yyyy.append(d.year) 
    mm.append(d.month)
    dd.append(d.day)
    hr.append(d.hour)
    mn.append(d.minute)
    ss.append(d.second)
    
yyyy = np.array(yyyy)
mm = np.array(mm)
dd = np.array(dd)
hr = np.array(hr)
mn = np.array(mn)
ss = np.array(ss)

##############################################################################################################################
#--- how to get it into Arcgis and google earth ---#

kmlobj = KML.kml(
    KML.Document(
    )
)   
 
for j in range(len(yyyy)):  #create the ref icons we will use
    kmlobj.Document.append(     
        KML.Style(             
            KML.IconStyle(
                KML.Icon(
                    KML.href('%s.png'%str(event_id[j])),
                    KML.scale(0.6),   #scale the beachball in googleEarth
                ),
                KML.heading(0.0),
            ),
        id='beach_ball_%s'%event_id[j]    #gives the icon a ref that will be used later
        ),
    )
 
# add images to the document element
for i in range(len(yyyy)):
    datum = str(date.date(int(yyyy[i]),int(mm[i]),int(dd[i])))
    ev_time = str(date.time(int(hr[i]),int(mn[i]),int(ss[i])))
    eventid = event_id[i]
    Mw = data['mw'][i]
    CD = data['CD'][i]
    Mo = data['mo'][i]
    
    kmlobj.Document.append(
        KML.Placemark(
            KML.name('%s'%str(eventid)),   #uncomment this to add a name to the placemark (will always appear in GoogleEarth)
            KML.ExtendedData(                       #I add information about the earthquake, it appears in a table ('info' : value)
                KML.Data(                           
                    KML.value('%s'%datum),          #add value of the specific info
                name ='date'                        #name of'info' you add.
                ),
                KML.Data(
                    KML.value('%s'%ev_time),        #add value of the specific info 
                name ='time'                        #name of 'info' you add.
                ),
                KML.Data(
                    KML.value('%s'%eventid), 
                name ='event_id'
                ),
                KML.Data(
                    KML.value('%s'%Mw), 
                name ='Mw'
                ),
                KML.Data(
                    KML.value('%s'%CD), 
                name ='CD'
                ),
                KML.Data(
                    KML.value('%s'%Mo), 
                name ='Mo'
                ),
            ),                                     #more data can be added, following the same structure 
            KML.styleUrl('#beach_ball_%s'%eventid),       #get the correct beachball in the directory as marker
            KML.Point(
                KML.coordinates(longitude[i],',',latitude[i]),
            ),
 
        ),
    )
 
print etree.tostring(etree.ElementTree(kmlobj),pretty_print=True)
outfile= file(kmlout,'w') #save the kml structure code
outfile.write(etree.tostring(kmlobj, pretty_print=True))

