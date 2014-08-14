"""
Created on Thu Aug 14 11:33:18 2014

@author: napo
"""
from dbxmlmibact import DBMibac,LuoghiCultura, Indirizzi, Extra, Allegati, Links
from managexmlmibac import MibacData
data = MibacData()
mibac = data.getalldata()
db = DBMibac(".","luoghicultura")

luoghi = []
for m in mibac:
    #Accessibilita(accessibilita=m.accessibilita)

    #links
    if len(m.links)>0:
        for link in m.links:
            if (len(link)>0):
                for l in link:
                    linkssql = Links(codice_dbunico2=m.codice_dbunico2,url=l['url'],titolo=l['titolo'],descrizione=l['descrizione'],tipo=l['tipo'])
                    db.add(linkssql)
    
    #Allegati
    #codice_dbunico2, copyright, url, ruolo, didascalia,mibacallegato,descrizione
    if len(m.allegati)>0:
        for allegato in m.allegati:
            if (len(allegato)>0):
                allegatisql = Allegati(codice_dbunico2=m.codice_dbunico2,copyright=allegato['copyright'], url=allegato['url'], ruolo=allegato['ruolo'], 
                            didascalia=allegato['didascalia'],mibacidallegato=allegato['mibacidallegato'],descrizione=allegato['descrizione'])
                db.add(allegatisql)
    
    #Extra: tipologia,categoria,traduzioni varie, contenitori
    
    if (len(m.contenitori)>0):
        extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="contenitori",attributo='denominazione',m.contenitori['denominazione'])
        db.add(extrasql)
        
    if len(m.categorie) > 0:
        for c in range(len(m.categorie)):
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="categoria",attributo=c,valore=m.categorie[c])
            db.add(extrasql)
            
    if len(m.tipologie) > 0:
        for t in range(len(m.tipologie)):
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="tipologia",attributo=t,valore=m.tipologie[t])
            db.add(extrasql)

    if len(m.sinonimi) > 0:
        for s in range(len(m.sinonimi)):
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="sinomimo",attributo=s,valore=m.sinonimi[s])
            db.add(extrasql)
            
    if len(m.traduzioni_descrizione) > 0:
        for t in m.traduzioni_descrizione:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_descrizione",attributo=t,valore=m.traduzioni_descrizione[t])
            db.add(extrasql)

    if len(m.traduzioni_chiusurasettimanale) > 0:
        for t in m.traduzioni_chiusurasettimanale:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_chiusurasettimanale",attributo=t,valore=m.traduzioni_chiusurasettimanale[t])
            db.add(extrasql)

    if len(m.traduzioni_costo_biglietto) > 0:
        for t in m.traduzioni_costo_biglietto:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_costo_biglietto",attributo=t,valore=m.traduzioni_costo_biglietto[t])
            db.add(extrasql)         

    if len(m.traduzioni_fax_biglietteria) > 0:
        for t in m.traduzioni_fax_biglietteria:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_costo_biglietto",attributo=t,valore=m.traduzioni_fax_biglietteria[t])
            db.add(extrasql)       
        
    if len(m.traduzioni_orario) > 0:
        for t in m.traduzioni_orario:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_orario",attributo=t,valore=m.traduzioni_orario[t])
            db.add(extrasql)  
 
    if len(m.traduzioni_orario_biglietteria) > 0:
        for t in m.traduzioni_orario_biglietteria:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_orario_biglietteria",attributo=t,valore=m.traduzioni_orario_biglietteria[t])
            db.add(extrasql)     
    

    if len(m.traduzioni_prenotazioni_telefono) > 0:
        for t in m.traduzioni_prenotazioni_telefono:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_prenotazioni_telefono",attributo=t,valore=m.traduzioni_prenotazioni_telefono[t])
            db.add(extrasql)     

    if len(m.traduzioni_telefono) > 0:
        for t in m.traduzioni_telefono:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_telefono",attributo=t,valore=m.traduzioni_telefono[t])
            db.add(extrasql)     
    
    if len(m.traduzioni_telefono_biglietteria) > 0:
        for t in m.traduzioni_telefono_biglietteria:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_telefono_biglietteria",attributo=t,valore=m.traduzioni_telefono_biglietteria[t])
            db.add(extrasql) 

    if len(m.traduzioni_riduzioni_biglietto) > 0:
        for t in m.traduzioni_riduzioni_biglietto:
            extrasql = Extra(codice_dbunico2=m.codice_dbunico2,tipo="traduzioni_riduzioni_biglietto",attributo=t,valore=m.traduzioni_riduzioni_biglietto[t])
            db.add(extrasql) 

            
    if len(m.indirizzi) > 0:    
        for ind in m.indirizzi:
            point='POINT(%s %s)' % (ind['longitudine'],ind['latitudine'])
            indirizzosql = Indirizzi(codice_dbunico2=m.codice_dbunico2, indirizzo=ind['indirizzo'], 
                            cap=ind['cap'], comune=ind['comune'], localita=ind['localita'], provincia=ind['provincia'], 
                            regione=ind['regione'], latitudine=ind['latitudine'], longitudine=ind['longitudine'], 
                            istat_comune=ind['istat_comune'], istat_provincia=ind['istat_provincia'], 
                            istat_regione=ind['istat_regione'], geom=point)
            db.add(indirizzosql)  
            
    point='POINT(%s %s)' % (m.longitudine,m.latitudine)
    luoghiculturasql = LuoghiCultura(cap=m.cap,categoria=m.categoria,chiusurasettimanale=m.chiusurasettimanale,
        codice_dbunico2=m.codice_dbunico2, codice_entecompetente_dbunico20=m.codice_entecompetente_dbunico20,
        codice_entecompetente_mibac=m.codice_entecompetente_mibac,codice_entegestore_dbunico20=m.codice_entegestore_dbunico20,
        codice_entegestore_mibac=m.codice_entegestore_mibac,comune=m.comune,costo_biglietto=m.costo_biglietto,
        data_validazione=m.data_validazione,data_ultima_modifica=m.data_ultima_modifica,
        data_creazione_xml=m.data_creazione_xml,descrizione=m.descrizione, email=m.email, email_biglietteria=m.email_biglietteria,
        email_certificata=m.email_certificata, entecompetente=m.entecompetente,entecompilatore=m.entecompilatore,entegestore=m.entegestore,
        fax=m.fax,fax_biglietteria=m.fax_biglietteria,idtipologialuogo=m.idtipologialuogo, img=m.img,indirizzo=m.indirizzo,istat_regione=m.istat_regione,
        istat_provincia=m.istat_provincia,istat_comune=m.istat_comune,latitudine=m.latitudine,localita=m.localita, longitudine=m.longitudine,
        nome_redattore=m.nome_redattore,nome_capo_redattore=m.nome_capo_redattore, nome=m.nome, orario=m.orario,  
        orario_biglietteria=m.orario_biglietteria, prenotazioni_sitoweb=m.prenotazioni_sitoweb,prenotazioni_email=m.prenotazioni_email,  
        prenotazioni_telefono=m.prenotazioni_telefono, proprieta=m.proprieta, provincia=m.provincia,responsabile=m.responsabile,   
        regione=m.regione, riduzioni_biglietto=m.riduzioni_biglietto, ruolo_entecompetente=m.ruolo_entecompetente,   
        ruolo_entegestore=m.ruolo_entegestore, stato=m.stato, sitoweb=m.sitoweb, sorgente=m.sorgente, telefono=m.telefono,
        telefono_biglietteria=m.telefono_biglietteria, tipologia=m.tipologia,tipologialuogo=m.tipologialuogo, tipo_prenotazioni=m.tipo_prenotazioni,
        geom=point)  
    db.add(luoghiculturasql)                                 
db.session.commit()
                           
