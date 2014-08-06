import urllib2
from lxml import etree
import csv
import django.utils.encoding as djenc
filename="luoghicultura.csv"
url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&tipologiaLuogo=1&stato=P&quantita=1&offset=0"
#url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&stato=P&quantita=1&offset=0"

xml = urllib2.urlopen(url)
root = etree.parse(xml)
totmuseums = int(root.getroot().attrib['totale'])
print totmuseums
limit = 1000
steps=totmuseums/limit


idx = []

if (totmuseums%limit>0):
    steps += 1
    

for s in range(steps):
    idx.append(s*limit)
step = 0

with open(filename, 'wb') as csvfile:
    museiwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    museiwriter.writerow(["nome","indirizzo","comune","provincia","cap","sitoweb","latitudine","longitudine"])

for i in idx:
    index = idx.index(i)
    print index    
    url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&stato=P&offset=%s" % (index) 
#    url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&tipologiaLuogo=1&stato=P&offset=%s&quantita=1000" % (index)      
    xml = urllib2.urlopen(url)
    docxml = etree.parse(xml).findall("mibac")
    with open(filename, 'a') as csvfile:
        museiwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for mibac in docxml:
            writerow = []
            metainfo = mibac.find('metainfo')
            stato = ''
            if (metainfo.find('workflow/stato') != None):
                stato = metainfo.find('workflow/stato').text
            enteCompilatore = ''
            if (metainfo.find('workflow/enteCompilatore') != None):
                enteCompilatore = metainfo.find('workflow/enteCompilatore').text
            nomeRedattore = ''
            if (metainfo.find('workflow/nomeRedattore') != None):
                nomeRedattore = metainfo.find('workflow/nomeRedattore').text
            nomeCapoRedattore = ''
            if (metainfo.find('workflow/nomeCapoRedattore') != None):
                nomeCapoRedattore = metainfo.find('workflow/nomeCapoRedattore').text
            dataValidazione = ''
            if (metainfo.find('workflow/dataValidazione') != None):
                dataValidazione = metainfo.find('workflow/dataValidazione').text
            dataUltimaModifica = ''
            if (metainfo.find('workflow/dataUltimaModifica') != None):
                dataValidazione = metainfo.find('workflow/dataUltimaModifica').text
            datacreazionexml = ''
            if (metainfo.find('datacreazionexml') != None):
                datacreazionexml = metainfo.find('datacreazionexml').text
            sorgente =''
            if (metainfo.find('sorgente') != None):
                datacreazionexml = metainfo.find('sorgente').text
            luogodellacultura = mibac.find("luogodellacultura")
            codice = luogodellacultura.find("identificatore/codice").text
            tipologiaprevalente = luogodellacultura.find("tipologie").attrib['tipologiaPrevalente']
            if (len(luogodellacultura.find("tipologie").attrib)) > 1:
                print "altre tipologie"
            categoriaprevalente = luogodellacultura.find("categorie").attrib['categoriaPrevalente']
            if (len(luogodellacultura.find("categorie").attrib)) > 1:
                print "altre categorie"
            proprieta = luogodellacultura.find("proprieta").text
            nomestandard = luogodellacultura.find("denominazione/nomestandard").text
            nome = nomestandard.replace('"','')        
            sinomimi = luogodellacultura.find("denominazione/sinonimi").getchildren()
            if len(sinomimi) > 0:
                print "altri sinomimi" 
            descrizione = ''
            if (luogodellacultura.find("descrizione/testostandard") != None):
                descrizione = luogodellacultura.find("descrizione/testostandard").text
                traduzioni = luogodellacultura.find("descrizione/traduzioni").getchildren()
                if len(traduzioni) > 0:
                    print "altre traduzioni"
    
            info = luogodellacultura.find("info")
            orario = ""
            orario_traduzioni = ""
            if (info != None):
                if (info.find("orario/testostandard") != None):
                    orario = info.find("orario/testostandard").text
                    orario_traduzioni = info.find("orario/traduzioni").getchildren()
                    if (len(orario_traduzioni) > 0):
                        print "orario multilingue"
                responsabile = info.find("responsabile").text
                accessibilita = info.find("accessibilita").text
                sitoweb = info.find("sitoweb").text
                email = info.find("email").text
                email_certificata = ""
                email_certificata = info.find("email-certificata").text
                telefono = info.find("telefono/testostandard").text
                telefono_traduzioni = info.find("telefono/traduzioni").getchildren()
                if (len(telefono_traduzioni)) > 0:
                    print "altre traduzioni telefono"
                fax = info.find("fax/testostandard").text
                fax_traduzioni = info.find("fax/traduzioni").getchildren()
                if (len(fax_traduzioni)) > 0:
                    print "altre traduzioni fax" 
                if (info.find("chiusuraSettimanale/testostandard") != None):
                    chiusurasettimanale = info.find("chiusuraSettimanale/testostandard").text
                    chiusurasettimanale_traduzioni = info.find("chiusuraSettimanale/traduzioni").getchildren()
                    if (len(chiusurasettimanale_traduzioni)) > 0:
                        print "altre traduzioni chiusuraSettimanale" 
    
            if (luogodellacultura.find("enteCompetente") != None):
                entecompetente = luogodellacultura.find("enteCompetente/denominazione").text
                ruolo_entecompetente = luogodellacultura.find("enteCompetente").attrib['ruolo']
                codici = luogodellacultura.find("enteCompetente/identificatore").getchildren()
                codice_entecompetente_dbunico20 = ""   
                codice_entecompetente_mibac = ""
                for codice in codici:
                    if (codice.attrib['sorgente']=='DBUnico2.0'):
                        codice_entecompetente_dbunico20 = codice.text
                    if (codice.attrib['sorgente']=='MiBAC'):
                        codice_entecompetente_mibac = codice.text
                entegestore = ""
                ruolo_entegestore = ""
                codice_entegestore_dbunico20 = ""
                codice_entegestore_mibac = ""
                
            if (luogodellacultura.find("enteGestore/denominazione") != None):
                entegestore = luogodellacultura.find("enteGestore/denominazione").text
                ruolo_entegestore = luogodellacultura.find("enteGestore").attrib['ruolo']
                codici = luogodellacultura.find("enteGestore/identificatore").getchildren()
                codice_entegestore_dbunico20 = ""   
                codice_entegestore_mibac = ""
                for codice in codici:
                    if (codice.attrib['sorgente']=='DBUnico2.0'):
                        codice_entegestore_dbunico20 = codice.text
                    if (codice.attrib['sorgente']=='MiBAC'):
                        codice_entegestore_mibac = codice.text
    
            contenitori = luogodellacultura.find("contenitori").getchildren()
            if (len(contenitori)>0):
                print "Ci sono contenitori"
        
            biglietteria = luogodellacultura.find("biglietteria")
            telefono_biglietteria = ""
            fax_biglietteria = ""
            email_biglietteria = ""
            costo_biglietto = ""
            riduzioni_biglietto = ""
            orario_biglietteria = ""
            if (biglietteria != None):
                telefono_biglietteria = biglietteria.find("telefono-biglietteria/testostandard").text
                telefono_biglietteria_traduzioni = biglietteria.find("telefono-biglietteria/traduzioni").getchildren()
                if (len(telefono_biglietteria_traduzioni)) > 0:
                    print "altre traduzioni telefono_biglietteria"  
                fax_biglietteria = biglietteria.find("fax-biglietteria/testostandard").text
                fax_biglietteria_traduzioni = biglietteria.find("fax-biglietteria/traduzioni").getchildren()
                if (len(fax_biglietteria_traduzioni)) > 0:
                    print "altre traduzioni fax_biglietteria"  
                email_biglietteria = biglietteria.find("email-biglietteria").text
                costo_biglietto = biglietteria.find("costo").text
                costo_biglietto_traduzioni = biglietteria.find("costo/traduzioni").getchildren()
                if (len(costo_biglietto_traduzioni)) > 0:
                    print "altre traduzioni costo_biglietto_traduzioni" 
                riduzioni_biglietto = biglietteria.find("riduzioni").text
                riduzioni_biglietto_traduzioni = biglietteria.find("riduzioni/traduzioni").getchildren()
                if (len(riduzioni_biglietto_traduzioni)) > 0:
                    print "altre traduzioni riduzioni_biglietto_traduzioni" 
                orario_biglietteria = biglietteria.find("orario-biglietteria").text
                if (biglietteria.find("orario-biglietteria/traduzioni") != None):
                    orario_biglietteria_traduzioni = biglietteria.find("orario-biglietteria/traduzioni").getchildren()
                    if (len(orario_biglietteria_traduzioni)) > 0:
                        print "altre traduzioni orario_biglietteria_traduzioni"
        
            if (luogodellacultura.find("prenotazioni") != None):
                tipo_prenotazioni = ""
                if len(luogodellacultura.find("prenotazioni").attrib) > 0:
                    tipo_prenotazioni = luogodellacultura.find("prenotazioni").attrib['tipo']
                prenotazioni_sitoweb = luogodellacultura.find("prenotazioni/sitoweb").text
                prenotazioni_email = luogodellacultura.find("prenotazioni/email").text
                prenotazioni_telefono = luogodellacultura.find("prenotazioni/telefono").text
                prenotazioni_telefono_traduzioni = luogodellacultura.find("prenotazioni/telefono/traduzioni").getchildren()
                if (len(prenotazioni_telefono_traduzioni)) > 0:            
                    print "altre traduzioni prenotazioni_telefono_traduzioni" 
        
            indirizzi = luogodellacultura.find("indirizzi").getchildren()
            if (len(indirizzi) > 1):
                print "ci sono molti indirizzi"
            indirizzo = indirizzi[0]
            tipo_indirizzo = ""
            if len(indirizzo.attrib) > 0:
                tipo_indirizzo = indirizzo.attrib[indirizzo.attrib.keys()[0]]
            via_indirizzo = ""
            if (indirizzo.find('via-piazza') != None):
                via_indirizzo = indirizzo.find('via-piazza').text
            comune_indirizzo = ""
            codistat_comune_indirizzo = ""
            if (indirizzo.find('comune') != None):
                comune_indirizzo = indirizzo.find('comune').text
                codistat_comune_indirizzo = indirizzo.find('comune').attrib['istat']
            cap_indirizzo = ""
            if (indirizzo.find('cap') != None):
                cap_indirizzo = indirizzo.find('cap').text
            provincia_indirizzo = ""
            codistat_provincia_indirizzo = ""
            if (indirizzo.find('provincia') != None):
                provincia_indirizzo = indirizzo.find('provincia').text
                codistat_provincia_indirizzo = indirizzo.find('provincia').attrib['istat'] 
            if (indirizzo.find('regione') != None):
                regione_indirizzo = indirizzo.find('regione').text
                codistat_regione_indirizzo = indirizzo.find('regione').attrib['istat'] 
            latitudine = ""
            longitudine = ""
            if (indirizzo.find('cartografia') != None):
                latitudine = indirizzo.find('cartografia/punto/latitudineX').text
                longitudine = indirizzo.find('cartografia/punto/longitudineY').text
            links = luogodellacultura.find("links")
            print links.getchildren()
            allegati = luogodellacultura.find("allegati")
            print allegati.getchildren()
            step += 1
            if (longitudine != ""):
                writerow.append(djenc.smart_str(nome))        
                writerow.append(djenc.smart_str(via_indirizzo))
                writerow.append(djenc.smart_str(comune_indirizzo))
                writerow.append(djenc.smart_str(provincia_indirizzo))
                writerow.append(djenc.smart_str(cap_indirizzo))
                writerow.append(djenc.smart_str(sitoweb))
                writerow.append(djenc.smart_str(latitudine))
                writerow.append(djenc.smart_str(longitudine))
                museiwriter.writerow(writerow)

