# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 20:55:25 2014

@author: Maurizio Napolitano <napo@fbk.eu>
"""
import urllib2
import urllib
import geojson
import json

class Nominatim():
    defaultprovider='mapquest'
    output='json'
    
    def __init__(self):
        services = {}
        services['mapquest'] = 'http://open.mapquestapi.com/nominatim/v1/search/'
        services['nominatim'] = 'http://nominatim.openstreetmap.org/search?'
        self.services = services
        
    def query(self,query,housenumber=None,street=None,city=None,
                      country=None,state=None,postalcode=None,viewbox=None,
                      limit=None,bounded=0,polygon_text=0,addressdetails=0,provider=defaultprovider):     
        values={}
        #values['q']=query   
        if housenumber is not None and street is not None:
            v = "%s %s" % (housenumber,street)
            values['street']=v
        if street is not None and housenumber is None:
            values['street']=street
        if city is not None:
            values['city']=city
        print country
        if country is not None:
            values['country']=country
        if state is not None:
            values['state']=state
        if postalcode is not None:
            values['postalcode']=postalcode
        if viewbox is not None:
            if len(viewbox) == 4:
                values['viewbox']=viewbox
        values['format']='json'
        parameters = urllib.urlencode(values)
        url = self.services[provider] + query + '?' + parameters
        print url
        response = urllib2.urlopen(url)
        return json.load(response)
                
        
class Photon():        
    def query(self,q,lang='it',lat=None,lon=None,limit=None):
        values = {}
        values['q']=q
        #geoposition = ''
        #limits=''
        #lang = "&lang=%s" % lang
        #values={'q':q}    
        url='http://photon.komoot.de/api/?'
        if (lat is not None and lon is not None):
            #geoposition="&lon=%s&lat=%s"  % (lon,lat)
            values['lon']=lon
            values['lat']=lat
        if (limit is not None):
            #limits = '&limit=%s' % limit
            values['limit']=limit
        values['lang']=lang
        query = urllib.urlencode(values)
        url = url + query
        #url = url + query + lang + geoposition + limits
        response = urllib2.urlopen(url)
        return geojson.load(response)

