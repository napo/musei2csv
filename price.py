# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 23:39:14 2014

@author: napo
"""
import os
from dbxmlmibact import DBMibac,LuoghiCultura
db = DBMibac(os.getcwd(),"luoghicultura")

biglietti = db.session.query(LuoghiCultura.costo_biglietto).distinct()
for costo in biglietti.all():
    print costo[0]


def findpricefromeuro(costo):
    price = -1
    prices=[]
    euri = costo.split(' ')
    for euro in euri:
        if euro != '':
            if (isprice(euro)):
                euro = euro.replace(',','.')
                euro = euro.replace('€','')
                euro = euro.replace(";",'')
                euro = euro.replace("museo","")
                addzero = euro.find('.')
                if addzero > -1:
                    afterzero = euro[addzero:len(euro)]
                    if len(afterzero) == 1:
                        euro += "0"
                prices.append(float(euro))
    if len(prices)>0:
        for p in prices:
            if p > price:
                price = p
    return price
                
                    
def isprice(price):
    rp=False
    if ((len(price)>2) and price.find("€")) > -1:
        for p in range(len(price)):
            if price[p].isdigit():    
                rp=True
                break
    else:
        rp=False
        results = []
        for p in range(len(price)):
            v = price[p]
            if v.isdigit():
                rp = True
            if v=="," or v==".":
                if p>0:
                    pv = price[p-1]
                    if pv.isdigit():
                        rp=True
            else:
                rp = False
            results.append(rp)
        for r in results:
            if (r==False):
                rp = False
                break
    return rp