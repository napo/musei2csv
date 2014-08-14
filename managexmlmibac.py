# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 19:33:28 2014

@author: Maurizio Napolitano
"""
import urllib2
from lxml import etree
import django.utils.encoding as djenc

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
    def __init__(self,inmibac,idtipologialuogo,tipologialuogo):
        self.accessibilita = ""
        self.allegati = []
        self.cap = ""
        self.categoria = ""
        self.categorie = []
        self.chiusurasettimanale = ""        
        self.codice_dbunico2 = ""
        self.codice_entecompetente_dbunico20 = ""
        self.codice_entecompetente_mibac = ""   
        self.codice_entegestore_dbunico20 = ""
        self.codice_entegestore_mibac = ""
        self.comune = ""
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
        self.entecompilatore = ""
        self.entegestore = ""
        self.fax = ""
        self.fax_biglietteria = ""
        self.idtipologialuogo = idtipologialuogo
        self.img = ""
        self.indirizzi = []
        self.indirizzo = ""
        self.istat_regione = ""
        self.istat_provincia = ""
        self.istat_comune = ""
        self.latitudine = ""
        self.links = []
        self.localita = ""
        self.longitudine = ""
        self.nome_redattore = ""
        self.nome_capo_redattore = ""
        self.nome = ""
        self.orario = "" 
        self.orario_biglietteria = ""    
        self.prenotazioni_sitoweb = ""
        self.prenotazioni_email = ""
        self.prenotazioni_telefono = ""
        self.proprieta = ""
        self.provincia = ""   
        self.responsabile = ""
        self.regione = ""
        self.riduzioni_biglietto = ""    
        self.ruolo_entecompetente = ''
        self.ruolo_entegestore = ""
        self.stato = ""
        self.sinonimi = []
        self.sitoweb = ""
        self.sorgente = ""
        self.telefono = ""
        self.telefono_biglietteria = ""
        self.tipologialuogo = tipologialuogo
        self.tipologia = ""
        self.tipologie = []
        self.traduzioni_descrizione = {}
        self.traduzioni_orario = {}
        self.traduzioni_telefono = {}
        self.traduzioni_fax= {}
        self.traduzioni_chiusurasettimanale= {}
        self.traduzioni_orario_biglietteria = {}
        self.traduzioni_telefono_biglietteria = {}
        self.traduzioni_fax_biglietteria = {} 
        self.traduzioni_costo_biglietto = {}
        self.traduzioni_riduzioni_biglietto = {}
        self.traduzioni_prenotazioni_telefono = {}
        self.tipo_prenotazioni = ""
        self.riduzioni_biglietto = ""
        self.mibacxml = inmibac


        mibac = inmibac

        #METAINFO
        metainfo = mibac.find('metainfo')
        if (metainfo.find('workflow/stato') is not None):
            self.stato = djenc.smart_str(metainfo.find('workflow/stato').text)
        if (metainfo.find('workflow/enteCompilatore') is not None):
            self.entecompilatore = djenc.smart_str(metainfo.find('workflow/enteCompilatore').text)
        if (metainfo.find('workflow/nomeRedattore') is not None):
            self.nome_redattore = djenc.smart_str(metainfo.find('workflow/nomeRedattore').text)
        if (metainfo.find('workflow/nomeCapoRedattore') is not None):
            self.nome_capo_redattore = djenc.smart_str(metainfo.find('workflow/nomeCapoRedattore').text)
        if (metainfo.find('workflow/dataValidazione') is not None):
            self.data_validazione = djenc.smart_str(metainfo.find('workflow/dataValidazione').text)
        if (metainfo.find('workflow/dataUltimaModifica') is not None):
            self.data_ultima_modifica = djenc.smart_str(metainfo.find('workflow/dataUltimaModifica').text)
        if (metainfo.find('datacreazionexml') is not None):
            self.data_creazione_xml = djenc.smart_str(metainfo.find('datacreazionexml').text)
        if (metainfo.find('sorgente') is not None):
            self.sorgente = djenc.smart_str(metainfo.find('sorgente').text)
        
        #LUOGODELLACULTURA
        luogodellacultura = mibac.find("luogodellacultura")
        codici = luogodellacultura.find("identificatore").getchildren()
        for codice in codici:
            if codice.attrib['sorgente'] == 'DBUnico 2.0':
                self.codice_dbunico2 = djenc.smart_str(codice.text)
        self.tipologia = luogodellacultura.find("tipologie").attrib['tipologiaPrevalente']
        xtipologie = luogodellacultura.find("tipologie")
        if (len(xtipologie)>0):
            for t in range(len(xtipologie)):
                self.tipologie.append(djenc.smart_str(xtipologie[t].text))
                
        self.categoria = luogodellacultura.find("categorie").attrib['categoriaPrevalente']
        xcategorie = luogodellacultura.find("categorie")
        if (len(xcategorie)>0):
            for t in range(len(xcategorie)):
                self.categorie.append(djenc.smart_str(xcategorie[t].text))
                
        self.proprieta = djenc.smart_str(luogodellacultura.find("proprieta").text)
        nomestandard = luogodellacultura.find("denominazione/nomestandard").text
        self.nome = nomestandard.replace('"','')        
        
        sinomimi = luogodellacultura.find("denominazione/sinonimi").getchildren()        
        if len(sinomimi) > 0:
            for sinonimo in luogodellacultura.find("denominazione/sinonimi").getchildren():
                self.sinonimi.append(djenc.smart_str(sinonimo.text))
        
        if (luogodellacultura.find("descrizione/testostandard") is not None):
            self.descrizione = djenc.smart_str(luogodellacultura.find("descrizione/testostandard").text)
            traduzioni = luogodellacultura.find("descrizione/traduzioni").getchildren()
            if len(traduzioni) > 0:
                for traduzione in traduzioni:
                    self.traduzioni_descrizione[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)
       
        info = luogodellacultura.find("info")
        if (info is not None):
            if (info.find("orario/testostandard") is not None):
                self.orario = info.find("orario/testostandard").text
                orario_traduzioni = info.find("orario/traduzioni").getchildren()
                if (len(orario_traduzioni) > 0):
                    for traduzione in orario_traduzioni:
                        self.traduzioni_orario[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)
                        
            self.responsabile = djenc.smart_str(info.find("responsabile").text)
            self.accessibilita = djenc.smart_str(info.find("accessibilita").text)
            self.sitoweb = djenc.smart_str(info.find("sitoweb").text)
            self.email = djenc.smart_str(info.find("email").text)
            self.email_certificata = djenc.smart_str(info.find("email-certificata").text)
            if info.find("telefono").getchildren():
                self.telefono = djenc.smart_str(info.find("telefono/testostandard").text)
                
            telefono_traduzioni = info.find("telefono/traduzioni").getchildren()               
            if (len(telefono_traduzioni) > 0):
                for traduzione in telefono_traduzioni:
                    self.traduzioni_telefono[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)

            self.fax = djenc.smart_str(info.find("fax/testostandard").text)            
            fax_traduzioni = info.find("fax/traduzioni").getchildren()            
            if (len(fax_traduzioni)) > 0:
                for traduzione in fax_traduzioni:
                    self.traduzioni_fax[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)
                    
            if (info.find("chiusuraSettimanale/testostandard") is not None):
                self.chiusurasettimanale = djenc.smart_str(info.find("chiusuraSettimanale/testostandard").text)
                chiusurasettimanale_traduzioni = info.find("chiusuraSettimanale/traduzioni").getchildren()
                if (len(chiusurasettimanale_traduzioni)) > 0:
                    for traduzione in chiusurasettimanale_traduzioni:
                        self.traduzioni_chiusurasettimanale[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)
        
        if (luogodellacultura.find("enteCompetente") is not None):
            self.entecompetente = djenc.smart_str(luogodellacultura.find("enteCompetente/denominazione").text)
            self.ruolo_entecompetente = djenc.smart_str(luogodellacultura.find("enteCompetente").attrib['ruolo'])
            codici = luogodellacultura.find("enteCompetente/identificatore").getchildren()

            for codice in codici:
                if (codice.attrib['sorgente']=='DBUnico2.0'):
                    self.codice_entecompetente_dbunico20 = djenc.smart_str(codice.text)
                if (codice.attrib['sorgente']=='MiBAC'):
                    self.codice_entecompetente_mibac = djenc.smart_str(codice.text)
                                
        if (luogodellacultura.find("enteGestore/denominazione") is not None):
            self.entegestore = djenc.smart_str(luogodellacultura.find("enteGestore/denominazione").text)
            self.ruolo_entegestore = djenc.smart_str(luogodellacultura.find("enteGestore").attrib['ruolo'])
            codici = luogodellacultura.find("enteGestore/identificatore").getchildren()

            for codice in codici:
                if (codice.attrib['sorgente']=='DBUnico2.0'):
                    self.codice_entegestore_dbunico20 = djenc.smart_str(codice.text)
                if (codice.attrib['sorgente']=='MiBAC'):
                    self.codice_entegestore_mibac = djenc.smart_str(codice.text)

        

        contenitori = luogodellacultura.find("contenitori").getchildren()
        if (len(contenitori)>0):
            for contenitore in contenitori:
                for c in contenitore:
                    self.contenitori[c.tag] = djenc.smart_str(c.text) 

               
        biglietteria = luogodellacultura.find("biglietteria")

        if (biglietteria is not None):
            self.telefono_biglietteria = djenc.smart_str(biglietteria.find("telefono-biglietteria/testostandard").text)
            telefono_biglietteria_traduzioni = biglietteria.find("telefono-biglietteria/traduzioni").getchildren()
            if (len(telefono_biglietteria_traduzioni)) > 0:
                for traduzione in telefono_biglietteria_traduzioni:
                    self.traduzioni_telefono_biglietteria[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)
                    
            self.fax_biglietteria = djenc.smart_str(biglietteria.find("fax-biglietteria/testostandard").text)
            fax_biglietteria_traduzioni = biglietteria.find("fax-biglietteria/traduzioni").getchildren()
            if (len(fax_biglietteria_traduzioni)) > 0:
                for traduzione in fax_biglietteria_traduzioni:
                    self.traduzioni_fax_biglietteria[traduzione.attrib['lingua']] = djenc.smart_str(traduzione.text)
 
            self.email_biglietteria = biglietteria.find("email-biglietteria").text
            if (biglietteria.find("costo/testostandard") is not None):
                self.costo_biglietto = djenc.smart_str(biglietteria.find("costo/testostandard").text)
           
            costo_biglietto_traduzioni = biglietteria.find("costo/traduzioni").getchildren() 
            if (len(costo_biglietto_traduzioni)) > 0:
                for traduzione in costo_biglietto_traduzioni:
                    testo = djenc.smart_str(traduzione.text)
                    lingua = traduzione.attrib[traduzione.keys()[0]]
                    self.traduzioni_costo_biglietto[lingua] = testo
            
            self.riduzioni_biglietto = djenc.smart_str(biglietteria.find("riduzioni").text)
            riduzioni_biglietto_traduzioni = biglietteria.find("riduzioni/traduzioni").getchildren()
            if (len(riduzioni_biglietto_traduzioni)) > 0:
                for traduzione in riduzioni_biglietto_traduzioni:
                    testo = djenc.smart_str(traduzione.text)
                    lingua = traduzione.attrib[traduzione.keys()[0]]
                    self.traduzioni_riduzioni_biglietto[lingua] = testo
            
            self.orario_biglietteria = biglietteria.find("orario-biglietteria").text
            if (biglietteria.find("orario-biglietteria/traduzioni") is not None):
                orario_biglietteria_traduzioni = biglietteria.find("orario-biglietteria/traduzioni").getchildren()
                if (len(orario_biglietteria_traduzioni)) > 0:
                    for traduzione in orario_biglietteria_traduzioni:
                        testo = djenc.smart_str(traduzione.text)
                        lingua = traduzione.attrib[traduzione.keys()[0]]
                        self.traduzioni_orario_biglietteria[testo] = lingua
    
        if (luogodellacultura.find("prenotazioni") is not None):
            if len(luogodellacultura.find("prenotazioni").attrib) > 0:
                self.tipo_prenotazioni = djenc.smart_str(luogodellacultura.find("prenotazioni").attrib['tipo'])
            self.prenotazioni_sitoweb = djenc.smart_str(luogodellacultura.find("prenotazioni/sitoweb").text)
            self.prenotazioni_email = djenc.smart_str(luogodellacultura.find("prenotazioni/email").text)
            self.prenotazioni_telefono = djenc.smart_str(luogodellacultura.find("prenotazioni/telefono").text)
            prenotazioni_telefono_traduzioni = luogodellacultura.find("prenotazioni/telefono/traduzioni").getchildren()
            if (len(prenotazioni_telefono_traduzioni)) > 0:            
                for traduzione in prenotazioni_telefono_traduzioni:
                    testo = djenc.smart_str(traduzione.text)
                    lingua = traduzione.attrib[traduzione.keys()[0]]
                    self.traduzioni_prenotazioni_telefono[testo] = lingua
        
        xmlindirizzi = luogodellacultura.find("indirizzi")
        nindirizzi = 0

        for xmlindirizzo in xmlindirizzi:
            xtipo_indirizzo = ""
            xindirizzo = ""
            xlocalita = ""
            xcomune = ""
            xistat_comune = ""
            xprovincia = ""
            xistat_provincia = ""
            xregione = ""
            xistat_regione = ""
            xcap = ""
            xlatitudine = ""
            xlongitudine = "" 
            storeindirizzi = {}           
            if (len(xmlindirizzo.attrib)>0):
                xtipo_indirizzo = djenc.smart_str(xmlindirizzo.attrib[xmlindirizzo.attrib.keys()[0]])
            if (xmlindirizzo.find('via-piazza') is not None):
                xindirizzo = djenc.smart_str(xmlindirizzo.find('via-piazza').text)
            if (xmlindirizzo.find('localita') is not None):
                xlocalita = djenc.smart_str(xmlindirizzo.find('localita').text)
            if (xmlindirizzo.find('comune') is not None):
                xcomune = djenc.smart_str(xmlindirizzo.find('comune').text)
                xistat_comune = djenc.smart_str(xmlindirizzo.find('comune').attrib['istat'])
            if (xmlindirizzo.find('cap') is not None):
                xcap = djenc.smart_str(xmlindirizzo.find('cap').text)    
            if (xmlindirizzo.find('provincia') is not None):
                xprovincia = djenc.smart_str(xmlindirizzo.find('provincia').text)
                xistat_provincia = djenc.smart_str(xmlindirizzo.find('provincia').attrib['istat']) 
            if (xmlindirizzo.find('regione') is not None):
                xregione = djenc.smart_str(xmlindirizzo.find('regione').text)
                xistat_regione = xmlindirizzo.find('regione').attrib['istat'] 
            if (xmlindirizzo.find('cartografia') is not None):
                xlatitudine = djenc.smart_str(xmlindirizzo.find('cartografia/punto/latitudineX').text)
                xlongitudine = djenc.smart_str(xmlindirizzo.find('cartografia/punto/longitudineY').text)

            storeindirizzi['tipo']= xtipo_indirizzo
            storeindirizzi['indirizzo'] = xindirizzo
            storeindirizzi['localita'] = xlocalita 
            storeindirizzi['comune'] = xcomune
            storeindirizzi['istat_comune'] = xistat_comune
            storeindirizzi['provincia'] = xprovincia
            storeindirizzi['istat_provincia'] = xistat_provincia
            storeindirizzi['regione'] = xregione
            storeindirizzi['istat_regione'] = xistat_regione
            storeindirizzi['cap'] = xcap
            storeindirizzi['latitudine'] = xlatitudine 
            storeindirizzi['longitudine'] = xlongitudine
            self.indirizzi.append(storeindirizzi)      
            if nindirizzi == 0:
                self.indirizzo = xindirizzo
                self.localita = xlocalita
                self.comune = xcomune
                self.provincia = xprovincia
                self.cap = xcap
                self.regione = xregione
                self.istat_comune = xistat_comune
                self.istat_provincia = xistat_provincia
                self.istat_regione = xistat_regione
                self.latitudine = xlatitudine
                self.longitudine = xlongitudine             
            nindirizzi += 1
        

        links = luogodellacultura.find("links")
        store_links = []
        if (links.getchildren()>0):
            for link in links:
                store = {}
                if (link.attrib is not None):
                    store['tipo'] = djenc.smart_str(link.attrib['tipo'])
                for l in link.getchildren():
                    store[l.tag]=djenc.smart_str(l.text)
                store_links.append(store)
            self.links.append(store_links)                
        
        attachments = {}
        allegati = luogodellacultura.find("allegati")
        if (allegati is not None):
            for allegato in allegati:
                ruolo = djenc.smart_str(allegato.attrib["ruolo"])
                mibacidallegato = djenc.smart_str(allegato.attrib["mibacid"])
                for a in allegato:                   
                    attachments[a.tag]=djenc.smart_str(a.text)
                    if ruolo == "Immagine: Principale" and a.tag=="url":
                        self.img = djenc.smart_str(a.text)
                attachments["ruolo"] = ruolo
                attachments["mibacidallegato"] = mibacidallegato
            self.allegati.append(attachments)
    
        

