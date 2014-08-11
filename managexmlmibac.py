# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 19:33:28 2014

@author: Maurizio Napolitano
"""
import urllib2
from lxml import etree



class MibacData:
    tipologialuoghi = {}
    tipologialuoghi[1]="musei"
    tipologialuoghi[2]="aree_archeologice"
    tipologialuoghi[3]="parchi_archeologici"
    tipologialuoghi[4]="luoghi_culto"
    tipologialuoghi[5]="ville_palazzi"
    tipologialuoghi[6]="parchi_giardini"
    tipologialuoghi[7]="monumenti_funerari"
    tipologialuoghi[8]="architetture_forticate"
    tipologialuoghi[9]="architetture_civili"
    tipologialuoghi[10]="monumenti_archeologia_industriale"
    tipologialuoghi[11]="monumenti"
    tipologialuoghi[12]="altri"
    tipologialuoghi[13]="biblioteche"
    tipologialuoghi[20]="archivi"
    limit= 1000
    steps= {}
    totals = {}
    
    def __init__(self):
        for idtipoluogo in self.tipologialuoghi.keys():
            url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&stato=P&tipologiaLuogo=%s&quantita=1&offset=0" % (idtipoluogo)
            xml = urllib2.urlopen(url)
            root = etree.parse(xml)
            total = int(root.getroot().attrib['totale'])
            idx = []
            steps=total/self.limit
            if (total%self.limit>0):
                steps += 1 
            for s in range(steps):
                idx.append(s*self.limit)
                total/self.limit
            self.steps[idtipoluogo] = idx
            self.totals[idtipoluogo] = total

    def getmibacdata(self,idtipologialuogo,tipologialuogo,first,quantita=1000):
        mibacdata=[]
        tipologialuogo = self.tipologialuoghi[1]
        url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&stato=P&tipologiaLuogo=%s&quantita=%s&offset=%s" % (idtipologialuogo,quantita,first)
        xml = urllib2.urlopen(url)
        docxml = etree.parse(xml).findall("mibac")
        for data in docxml:
            mibac = Mibac(data,idtipologialuogo,tipologialuogo)
            mibacdata.append(mibac)
        return mibacdata  
    
    def getalldata(self):
        mibacdata=[]
        for idtipoluogo in self.tipologialuoghi.keys():
            tipologialuogo = self.tipologialuoghi[1]
            data = []
            for offset in self.steps[idtipoluogo]:
                data = self.getmibacdata(idtipoluogo,tipologialuogo,offset,self.limit)
                for d in data:
                    mibacdata.append(d)
        return mibacdata
        

class Mibac:  
    def __init__(self,inmibac,idtipologialuogo=1,tipologialuogo="musei"):
        self.mibacxml = None
        self.accessibilita = ""
        self.allegati = []
        self.cap_default = ""
        self.categoriaprevalente = ""
        self.categorie = {}
        self.chiusurasettimanale = ""        
        self.codice_dbunico2 = ""
        self.codice_entecompetente_dbunico20 = ""
        self.codice_entecompetente_mibac = ""   
        self.codice_entegestore_dbunico20 = ""
        self.codice_entegestore_mibac = ""
        self.comune_default = ""
        self.contenitori = {}
        self.costo_biglietto = ""
        self.data_validazione = ""
        self.data_ultima_modifica = ""
        self.data_creazione_xml = ""
        self.descrizione = ""    
        self.email = ""
        self.email_biglietteria = ""
        self.email_certificata = ""
        self.entecompetente = ""
        self.enteCompilatore = ""
        self.entegestore = ""
        self.fax = ""
        self.fax_biglietteria = ""
        self.idtipologialuogo = 1
        self.indirizzi = []
        self.indirizzo_default = ""
        self.istat_regione_default = ""
        self.istat_provincia_default = ""
        self.istat_comune_default = ""
        self.latitudine_default = ""
        self.links = []
        self.localita_default = ""
        self.longitudine_default = ""
        self.nome_redattore = ""
        self.nome_capo_redattore = ""
        self.nome = ""
        self.orario = "" 
        self.orario_biglietteria = ""    
        self.prenotazioni_sitoweb = ""
        self.prenotazioni_email = ""
        self.prenotazioni_telefono = ""
        self.proprieta = ""
        self.responsabile = ""
        self.ruolo_entecompetente = ''
        self.ruolo_entegestore = ""
        self.stato = ""
        self.sinonimi = []
        self.sitoweb = ""
        self.sorgente = ""
        self.telefono = ""
        self.telefono_biglietteria = ""
        self.telefono_biglietteria = ""
        self.tipologialuogo = "musei"
        self.tipologiaprevalente = ""
        self.tipologie = {}
        self.traduzioni_descrizione = {}
        self.traduzioni_orario = {}
        self.traduzioni_telefono = {}
        self.traduzioni_fax= {}
        self.traduzioni_chiusurasettimanale= {}
        self.traduzioni_telefono_biglietteria = {}
        self.traduzioni_fax_biglietteria = {} 
        self.traduzioni_costo_biglietto = {}
        self.traduzioni_riduzioni_biglietto = {}
        self.tipo_prenotazioni = ""
        self.tipo_prenotazioni = ""
        self.traduzioni_prenotazioni_telefono = ""
        self.riduzioni_biglietto = ""
        self.provincia_default = ""
        self.regione_default = ""
        self.riduzioni_biglietto = ""        
        
        self.mibacxml = inmibac
        self.idtipologialuogo = idtipologialuogo
        self.tipologialuogo = tipologialuogo
        mibac = inmibac
        
        #METAINFO
        metainfo = mibac.find('metainfo')
        if (metainfo.find('workflow/stato') is not None):
            self.stato = metainfo.find('workflow/stato').text
        if (metainfo.find('workflow/enteCompilatore') is not None):
            self.ente_compilatore = metainfo.find('workflow/enteCompilatore').text
        if (metainfo.find('workflow/nomeRedattore') is not None):
            self.nome_redattore = metainfo.find('workflow/nomeRedattore').text
        if (metainfo.find('workflow/nomeCapoRedattore') is not None):
            self.nome_capo_redattore = metainfo.find('workflow/nomeCapoRedattore').text
        if (metainfo.find('workflow/dataValidazione') is not None):
            self.data_validazione = metainfo.find('workflow/dataValidazione').text
        if (metainfo.find('workflow/dataUltimaModifica') is not None):
            self.data_ultima_modifica = metainfo.find('workflow/dataUltimaModifica').text
        if (metainfo.find('datacreazionexml') is not None):
            self.data_creazione_xml = metainfo.find('datacreazionexml').text
        if (metainfo.find('sorgente') is not None):
            self.sorgente = metainfo.find('sorgente').text
        
        #LUOGODELLACULTURA
        luogodellacultura = mibac.find("luogodellacultura")
        codici = luogodellacultura.find("identificatore").getchildren()
        for codice in codici:
            if codice.attrib['sorgente'] == 'DBUnico 2.0':
                self.codice_dbunico2 = codice.text
        self.tipologiaprevalente = luogodellacultura.find("tipologie").attrib['tipologiaPrevalente']
        if (len(luogodellacultura.find("tipologie").attrib)) > 1:
            for tipologia in luogodellacultura.find("tipologie").getchildren():
                self.tipologie[tipologia.attrib] = tipologia.text
        self.categoriaprevalente = luogodellacultura.find("categorie").attrib['categoriaPrevalente']
        if (len(luogodellacultura.find("categorie").attrib)) > 1:
            for categoria in luogodellacultura.find("categorie").getchildren():
                self.categorie[categoria.attrib] = categoria.text
        self.proprieta = luogodellacultura.find("proprieta").text
        nomestandard = luogodellacultura.find("denominazione/nomestandard").text
        self.nome = nomestandard.replace('"','')        
        
        sinomimi = luogodellacultura.find("denominazione/sinonimi").getchildren()        
        if len(sinomimi) > 0:
            for sinonimo in luogodellacultura.find("denominazione/sinonimi").getchildren():
                self.sinonimi.append(sinonimo.text)
        
        if (luogodellacultura.find("descrizione/testostandard") is not None):
            self.descrizione = luogodellacultura.find("descrizione/testostandard").text
            traduzioni = luogodellacultura.find("descrizione/traduzioni").getchildren()
            if len(traduzioni) > 0:
                for traduzione in traduzioni:
                    for testo in traduzione:
                        self.traduzioni_descrizione[testo.attrib['lingua']] = testo.text
        info = luogodellacultura.find("info")
        if (info is not None):
            if (info.find("orario/testostandard") is not None):
                self.orario = info.find("orario/testostandard").text
                orario_traduzioni = info.find("orario/traduzioni").getchildren()
                if (len(orario_traduzioni) > 0):
                    for traduzione in orario_traduzioni:
                        for testo in traduzione:
                            self.traduzioni_orario[testo.attrib['lingua']] = testo.text
            self.responsabile = info.find("responsabile").text
            self.accessibilita = info.find("accessibilita").text
            self.sitoweb = info.find("sitoweb").text
            self.email = info.find("email").text
            self.email_certificata = info.find("email-certificata").text
            if info.find("telefono").getchildren():
                self.telefono = info.find("telefono/testostandard").text
                
            telefono_traduzioni = info.find("telefono/traduzioni").getchildren()               
            if (len(telefono_traduzioni) > 0):
                for traduzione in telefono_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_telefono[testo.attrib['lingua']] = testo.text

            self.fax = info.find("fax/testostandard").text            
            fax_traduzioni = info.find("fax/traduzioni").getchildren()            
            if (len(fax_traduzioni)) > 0:
                for traduzione in fax_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_fax[testo.attrib['lingua']]=testo.text
                    
            if (info.find("chiusuraSettimanale/testostandard") is not None):
                self.chiusurasettimanale = info.find("chiusuraSettimanale/testostandard").text
                chiusurasettimanale_traduzioni = info.find("chiusuraSettimanale/traduzioni").getchildren()
                if (len(chiusurasettimanale_traduzioni)) > 0:
                    for traduzione in chiusurasettimanale_traduzioni:
                        for testo in traduzione:
                            self.traduzioni_chiusurasettimanale[testo.attrib['lingua']] = testo.text
        
        if (luogodellacultura.find("enteCompetente") is not None):
            self.entecompetente = luogodellacultura.find("enteCompetente/denominazione").text
            self.ruolo_entecompetente = luogodellacultura.find("enteCompetente").attrib['ruolo']
            codici = luogodellacultura.find("enteCompetente/identificatore").getchildren()

            for codice in codici:
                if (codice.attrib['sorgente']=='DBUnico2.0'):
                    self.codice_entecompetente_dbunico20 = codice.text
                if (codice.attrib['sorgente']=='MiBAC'):
                    self.codice_entecompetente_mibac = codice.text
                                
        if (luogodellacultura.find("enteGestore/denominazione") is not None):
            self.entegestore = luogodellacultura.find("enteGestore/denominazione").text
            self.ruolo_entegestore = luogodellacultura.find("enteGestore").attrib['ruolo']
            codici = luogodellacultura.find("enteGestore/identificatore").getchildren()

            for codice in codici:
                if (codice.attrib['sorgente']=='DBUnico2.0'):
                    self.codice_entegestore_dbunico20 = codice.text
                if (codice.attrib['sorgente']=='MiBAC'):
                    self.codice_entegestore_mibac = codice.text

        

        contenitori = luogodellacultura.find("contenitori").getchildren()
        if (len(contenitori)>0):
            for contenitore in contenitori:
                for c in contenitore:
                    self.contenitori[c.tag] = c.text 

               
        biglietteria = luogodellacultura.find("biglietteria")

        if (biglietteria is not None):
            self.telefono_biglietteria = biglietteria.find("telefono-biglietteria/testostandard").text
            telefono_biglietteria_traduzioni = biglietteria.find("telefono-biglietteria/traduzioni").getchildren()
            if (len(telefono_biglietteria_traduzioni)) > 0:
                for traduzione in telefono_biglietteria_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_telefono_biglietteria[testo.attrib['lingua']] = testo.text
                    
            self.fax_biglietteria = biglietteria.find("fax-biglietteria/testostandard").text
            fax_biglietteria_traduzioni = biglietteria.find("fax-biglietteria/traduzioni").getchildren()
            if (len(fax_biglietteria_traduzioni)) > 0:
                for traduzione in fax_biglietteria_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_fax_biglietteria[testo.attrib['lingua']] = testo.text
 
            self.email_biglietteria = biglietteria.find("email-biglietteria").text
            if (biglietteria.find("costo/testostandard") is not None):
                self.costo_biglietto = biglietteria.find("costo/testostandard").text
           
            costo_biglietto_traduzioni = biglietteria.find("costo/traduzioni").getchildren() 
            if (len(costo_biglietto_traduzioni)) > 0:
                for traduzione in costo_biglietto_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_costo_biglietto[testo.attrib['lingua']] = testo.text
            
            self.riduzioni_biglietto = biglietteria.find("riduzioni").text
            riduzioni_biglietto_traduzioni = biglietteria.find("riduzioni/traduzioni").getchildren()
            if (len(riduzioni_biglietto_traduzioni)) > 0:
                for traduzione in riduzioni_biglietto_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_riduzioni_biglietto[testo.attrib['lingua']] = testo.text
            
            self.orario_biglietteria = biglietteria.find("orario-biglietteria").text
            if (biglietteria.find("orario-biglietteria/traduzioni") is not None):
                orario_biglietteria_traduzioni = biglietteria.find("orario-biglietteria/traduzioni").getchildren()
                if (len(orario_biglietteria_traduzioni)) > 0:
                    for traduzione in orario_biglietteria_traduzioni:
                        for testo in traduzione:
                            self.traduzioni_orario_biglietteria[testo.attrib['lingua']] = testo.text
    
        if (luogodellacultura.find("prenotazioni") is not None):
            if len(luogodellacultura.find("prenotazioni").attrib) > 0:
                self.tipo_prenotazioni = luogodellacultura.find("prenotazioni").attrib['tipo']
            self.prenotazioni_sitoweb = luogodellacultura.find("prenotazioni/sitoweb").text
            self.prenotazioni_email = luogodellacultura.find("prenotazioni/email").text
            self.prenotazioni_telefono = luogodellacultura.find("prenotazioni/telefono").text
            prenotazioni_telefono_traduzioni = luogodellacultura.find("prenotazioni/telefono/traduzioni").getchildren()
            if (len(prenotazioni_telefono_traduzioni)) > 0:            
                for traduzione in prenotazioni_telefono_traduzioni:
                    for testo in traduzione:
                        self.traduzioni_prenotazioni_telefono[testo.attrib['lingua']] = testo.text  
        
        indirizzi = luogodellacultura.find("indirizzi")
        nindirizzi = 0
        storeindirizzi = {}
        for xmlindirizzo in indirizzi.getchildren():
            tipo_indirizzo = ""
            indirizzo = ""
            localita = ""
            comune = ""
            istat_comune = ""
            provincia = ""
            istat_provincia = ""
            regione = ""
            istat_regione = ""
            cap = ""
            latitudine = ""
            longitudine = ""            
            if (xmlindirizzo.attrib is not None):
                if (xmlindirizzo.attrib !=""):
                    tipo_indirizzo = xmlindirizzo.attrib[xmlindirizzo.attrib.keys()[0]]
            else:
                tipo_indirizzo = 'sede'
            if (xmlindirizzo.find('via-piazza') is not None):
                indirizzo = xmlindirizzo.find('via-piazza').text
            if (xmlindirizzo.find('localita') is not None):
                localita = xmlindirizzo.find('localita').text
            if (xmlindirizzo.find('comune') is not None):
                comune = xmlindirizzo.find('comune').text
                istat_comune = xmlindirizzo.find('comune').attrib['istat']
            if (xmlindirizzo.find('cap') is not None):
                cap = xmlindirizzo.find('cap').text    
            if (xmlindirizzo.find('provincia') is not None):
                provincia = xmlindirizzo.find('provincia').text
                istat_provincia = xmlindirizzo.find('provincia').attrib['istat'] 
            if (xmlindirizzo.find('regione') is not None):
                regione = xmlindirizzo.find('regione').text
                istat_regione = xmlindirizzo.find('regione').attrib['istat'] 
            if (xmlindirizzo.find('cartografia') is not None):
                latitudine = xmlindirizzo.find('cartografia/punto/latitudineX').text
                longitudine = xmlindirizzo.find('cartografia/punto/longitudineY').text

            storeindirizzi['tipo']= tipo_indirizzo
            storeindirizzi['indirizzo'] = indirizzo
            storeindirizzi['localita'] = localita 
            storeindirizzi['comune'] = comune
            storeindirizzi['istat_comune'] = istat_comune
            storeindirizzi['provincia'] = provincia
            storeindirizzi['istat_provincia'] = istat_provincia
            storeindirizzi['regione'] = regione
            storeindirizzi['istat_regione'] = istat_regione
            storeindirizzi['cap'] = cap
            storeindirizzi['latitudine'] = latitudine 
            storeindirizzi['longitudine'] = longitudine
            self.indirizzi.append(storeindirizzi)      
            if nindirizzi == 0:
                self.indirizzo_default = indirizzo
                self.localita_default = localita
                self.comune_default = comune
                self.provincia_default = provincia
                self.cap_default = cap
                self.regione_default = regione
                self.istat_comune_default = istat_comune
                self.istat_provincia_default = istat_provincia
                self.istat_regione = istat_regione
                self.latitudine_default = latitudine
                self.longitudine_default = longitudine             
            nindirizzi += 1
        
        store_links = []
        links = luogodellacultura.find("links")
        if (links.getchildren()>0):
            for link in links:
                store = {}
                if (link.attrib is not None):
                    store['tipo'] = link.attrib
                for l in link.getchildren():
                    store[l.tag]=l.text
                store_links.append(store)
                self.links.append(store_links)                
        
        attachments = {}
        allegati = luogodellacultura.find("allegati")
        if (allegati is not None):
            for allegato in allegati:
                store = {}
                ruolo = allegato.attrib["ruolo"]
                mibacidallegato = allegato.attrib["mibacid"]
                for a in allegato:                   
                    store[a.tag]=a.text
                attachments["ruolo"] = ruolo
                attachments["mibacidallegato"] = mibacidallegato
                attachments["data"] = store                
            self.allegati.append(attachments)
    
        

