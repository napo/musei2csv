# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 22:47:38 2014

@author: Maurizio Napolitano <napo@fbk.eu>
"""

import urllib
import urllib2
import json
from shapely.geometry import Point, Polygon, LineString

class OSMData():         
    mappingtags = {}
    mappingtags[1] = "tourism=museum" #musei 
    mappingtags[2] = "historic=archaeological_site" #aree_archeologiche
    mappingtags[3] = "historic=archaeological_site" #parchi_archeologici"
    mappingtags[4] = "amenity=place_of_worship" #luoghi_culto"
    mappingtags[5] = "tourism=attraction" #ville_palazzi"
    mappingtags[6] = "leisure=park" #parchi
    mappingtags[7]= "historic=memorial|historic=ruins" #
    mappingtags[8]= "historic=castle|tourism=attraction" #architetture_forticate"
    mappingtags[9]= "tourism=attraction" #architetture_civili"
    mappingtags[10]="museum=*" #monumenti_archeologia_industriale"
    mappingtags[11]= "historic=archaeological_site"  #monumenti"
    mappingtags[12]= "tourism=attraction"
    mappingtags[13]= "amenity=library" #biblioteche"
    mappingtags[20]="*" #archivi"
    
    def __init__(self,area,tag):      
        key,value = tag.split("=")
        idarea=self.nominatimArea(area)
        url='http://overpass-api.de/api/interpreter?'
        query='''
        <osm-script output="json" timeout="250">
          <id-query into="area" ref="%s" type="area"/>
          <union>
          <!--
            <query type="node">
              <has-kv k="%s" v="%s"/>
              <area-query from="area"/>
            </query>
            <query type="way">
              <has-kv k="tourism" v="museum"/>
              <area-query from="area"/>
            </query>
         -->
            <query type="relation">
              <has-kv k="tourism" v="museum"/>
              <area-query from="area"/>
            </query>
          </union>
          <print mode="body"/>
          <recurse type="down"/>
          <print mode="skeleton" order="quadtile"/>
        </osm-script>
        ''' % (idarea,key,value)
        values={'data':query}    
        ask= urllib.urlencode(values)
        response = urllib2.urlopen(url+ask)
        self.data = json.load(response)

    def nominatimArea(self,inarea):
        prefix='36000'
        url = "http://nominatim.openstreetmap.org/search?q=%s&format=json&polygon=1" % (inarea)
        response = urllib2.urlopen(url)
        data = json.load(response)
        osm_id = ''
        for d in data:
            if d['osm_type'] == 'relation':
                osm_id = d['osm_id']
                break
        if osm_id != '':
            osm_id = prefix + osm_id
        return osm_id

class OSMGeometry():
    def __init__(self,id,osmtype,ids,tags):
        self.id = id
        self.osmtype = osmtype
        self.ids = ids
        self.tags = tags        
        self.nodes = []

    def addnode(self,idnode,node):
        added = False
        for vid in self.ids:
            if vid == idnode:
                self.nodes.append(node)
                added = True
                break
        return added
    def addway(self,idway,way):
        added = False
        for vid in self.ids:
            if vid == idnode:
                self.nodes.append(node)
                added = True
                break
        return added
        
    def buildgeometry(self):
        self.geometry = object
        if len(self.ids > 0):
            if (self.osmtype=='node'):
                self.geometry = Point(self.nodes[0])
            if (self.osmtype=='way'):
                createline = True
                if self.tags.has_key('building'):
                    if self.tags['building']=='yes':
                        createline = False
                if self.tags.has_key('area'):
                    if self.tags['area']=='yes':
                        createline = False
                if createline:
                    self.geometry = LineString(self.nodes)
                else:
                    self.geometry = Polygon(self.nodes)
            else: #relation
                
        return self.geometry