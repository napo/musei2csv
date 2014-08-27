# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 16:31:24 2014

@author: Maurizio Napolitano <napo@fbk.eu>
"""
from dbxmlmibact import DBMibac, LuoghiCultura, Indirizzi
from photongeocoding import PhotonGeocoder
from geopy.geocoders import Nominatim
import os

db = DBMibac(os.getcwd(),"luoghicultura")
musei = db.tablequery(LuoghiCultura).filter(LuoghiCultura.idtipologialuogo==1).limit(10)
geocoder = PhotonGeocoder()
geolocator = Nominatim()
for m in musei:
    query = '%s %s %s' % (m.nome, m.comune, m.regione)
    photon = geocoder.geocode(query)
    nominatim = geolocator.geocode(query)
    if len(photon['features']) > 0:
        for f in photon['features']:
            key = f['properties']['osm_key']
            value = f['properties']['osm_value']
            if (f['properties'].has_key('city')):
                city = f['properties']['city']
                indi = db.tablequery(Indirizzi).filter(Indirizzi.codice_dbunico2==m.codice_dbunico2).all()
                if (key =='tourism' and value =='museum' and city == m.comune):
                    print query + ' ' + m.indirizzo
                    print f
                    if len(indi) > 0:
                        print "+++"
                        for i in indi:
                            print i.indirizzo
                    
                    print "---"
        