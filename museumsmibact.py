import urllib2
from lxml import etree
import csv
import django.utils.encoding as djenc
from pyspatialite import dbapi2 as db
 
filename="luoghicultura.csv"
dbfile="culturalplaces.sqlite"
#MUSEI url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&tipologiaLuogo=1&stato=P&quantita=1&offset=0"
url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&stato=P&quantita=1&offset=0"

xml = urllib2.urlopen(url)
root = etree.parse(xml)
totmuseums = int(root.getroot().attrib['totale'])
print totmuseums
totmuseums = 1
limit = 1 #00
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


#spatialite
conn = db.connect(dbfile)
cur = conn.cursor()
sql = 'SELECT InitSpatialMetadata()'
cur.execute(sql)
# table of locations
sql = '''
CREATE TABLE luoghi (
codice_dbunico2 INTEGER NOT NULL PRIMARY KEY,
stato TEXT,
nomeRedattore TEXT,
nomeCapoRedattore TEXT,
dataValidazione TEXT,
dataUltimaModifica TEXT,
datacreazionexml TEXT,
sorgente TEXT,
tipologia TEXT,
categoria TEXT,
proprieta TEXT,
nome TEXT NOT NULL,
descrizione TEXT,
orario TEXT,
responsabile TEXT,
accessibilita TEXT,
sitoweb TEXT,
email TEXT,
email_certificata TEXT,
telefono TEXT,
chiusurasettimanale TEXT,
entecompetente TEXT,
ruolo_entecompetente TEXT,
codice_entecompetente_dbunico20 TEXT,
codice_entecompetente_mibac TEXT,
entegestore TEXT,
ruolo_entegestore TEXT,
codice_entegestore_dbunico20 TEXT,
codice_entegestore_mibac TEXT,
telefono_biglietteria TEXT,
fax_biglietteria TEXT,
email_biglietteria TEXT,
costo_biglietto TEXT,
riduzioni_biglietto TEXT,
orario_biglietteria TEXT,
tipo_prenotazioni TEXT,
prenotazioni_sitoweb TEXT,
prenotazioni_email TEXT,
prenotazioni_telefono TEXT,
indirizzo TEXT,
comune TEXT,
localita TEXT,
provincia TEXT,
regione TEXT,
istat_regione TEXT,
istat_provincia TEXT,
istat_comune TEXT,
cap TEXT,
latitudine TEXT,
longitudine TEXT);
'''
cur.execute(sql)

sql = "SELECT AddGeometryColumn('POINT'," 
sql += "'geom', 4326, 'POINT', 'XY')"
print sql
cur.execute(sql)



sql = '''
CREATE TABLE indirizzi (
codice_dbunico2 INTEGER NOT NULL,
indirizzo TEXT,
comune TEXT,
localita TEXT,
provincia TEXT,
regione TEXT,
istat_regione TEXT,
istat_provincia TEXT,
istat_comune TEXT,
cap TEXT,
latitudine TEXT,
longitudine TEXT);
'''
cur.execute(sql)


sql = '''
CREATE TABLE tipologie (
codice_dbunico2 INTEGER NOT NULL,
tipo TEXT,
testo TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE categorie (
codice_dbunico2 INTEGER NOT NULL,
categoria TEXT,
testo TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE sinomimi (
codice_dbunico2 INTEGER NOT NULL,
sinomimo TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE traduzioni_descrizioni (
codice_dbunico2 INTEGER NOT NULL,
descrizione TEXT,
lingua TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE traduzioni_orario (
codice_dbunico2 INTEGER NOT NULL,
orario TEXT,
lingua TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE traduzioni_telefono (
codice_dbunico2 INTEGER NOT NULL,
telefono TEXT,
lingua TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE traduzioni_fax (
codice_dbunico2 INTEGER NOT NULL,
fax TEXT,
lingua TEXT);
'''
cur.execute(sql)

sql = '''
CREATE TABLE contenitori (
codice_dbunico2 INTEGER NOT NULL,
contenitore TEXT,
tipo TEXT);
'''
cur.execute(sql)


for i in idx:
    index = idx.index(i)   
    url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&stato=P&offset=%s" % (index) 
#musei    url = "http://dbunico20.beniculturali.it/DBUnicoManagerWeb/dbunicomanager/searchPlace?modulo=luoghi&tipologiaLuogo=1&stato=P&offset=%s&quantita=1000" % (index)      
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
            codici = luogodellacultura.find("identificatore").getchildren()
            codice_dbunico2 = ''
            for codice in codici:
                if codice.attrib['sorgente'] == 'DBUnico 2.0':
                    codice_dbunico2 = codice.text
            tipologiaprevalente = luogodellacultura.find("tipologie").attrib['tipologiaPrevalente']
            if (len(luogodellacultura.find("tipologie").attrib)) > 1:
                for tipologia in luogodellacultura.find("tipologie").getchildren():
                    print "%s => %s" % (tipologia.attrib,tipologia.text)
                    #FARE LA INSERT
            categoriaprevalente = luogodellacultura.find("categorie").attrib['categoriaPrevalente']
            if (len(luogodellacultura.find("categorie").attrib)) > 1:
                for categoria in luogodellacultura.find("categorie").getchildren():
                    print "%s => %s" % (categoria.attrib,categoria.text)
                    #FARE LA INSERT
            proprieta = luogodellacultura.find("proprieta").text
            nomestandard = luogodellacultura.find("denominazione/nomestandard").text
            nome = nomestandard.replace('"','')        
            sinomimi = luogodellacultura.find("denominazione/sinonimi").getchildren()
            
            if len(sinomimi) > 0:
                for sinonimo in luogodellacultura.find("denominazione/sinonimi").getchildren():
                    print "%s => %s" % (sinonimo.attrib,sinonimo.text)
                    #FARE LA INSERT
            descrizione = ''
            if (luogodellacultura.find("descrizione/testostandard") != None):
                descrizione = luogodellacultura.find("descrizione/testostandard").text
                traduzioni = luogodellacultura.find("descrizione/traduzioni").getchildren()
                if len(traduzioni) > 0:
                    for traduzione in luogodellacultura.find("denominazione/traduzioni").getchildren():
                        print "%s => %s" % (traduzione.attrib,traduzione.text)
                        #FARE LA INSERT
            info = luogodellacultura.find("info")
            orario = ""
            orario_traduzioni = ""
            if (info != None):
                if (info.find("orario/testostandard") != None):
                    orario = info.find("orario/testostandard").text
                    orario_traduzioni = info.find("orario/traduzioni").getchildren()
                    if (len(orario_traduzioni) > 0):
                        for traduzione in orario_traduzioni:
                            print "%s => %s" % (traduzione.attrib,traduzione.text)
                            #FARE LA INSERT
                responsabile = info.find("responsabile").text
                accessibilita = info.find("accessibilita").text
                sitoweb = info.find("sitoweb").text
                email = info.find("email").text
                email_certificata = ""
                email_certificata = info.find("email-certificata").text
                telefono = info.find("telefono/testostandard").text
                telefono_traduzioni = info.find("telefono/traduzioni").getchildren()
               
                if (len(telefono_traduzioni) > 0):
                    for traduzione in telefono_traduzioni:
                        print "%s => %s" % (traduzione.attrib,traduzione.text)
                        #FARE LA INSERT
                fax = info.find("fax/testostandard").text
                fax_traduzioni = info.find("fax/traduzioni").getchildren()
                
                if (len(fax_traduzioni)) > 0:
                    for traduzione in fax_traduzioni:
                        print "%s => %s" % (traduzione.attrib,traduzione.text)
                        #FARE LA INSERT
                chiusurasettimanale = ''        
                if (info.find("chiusuraSettimanale/testostandard") != None):
                    chiusurasettimanale = info.find("chiusuraSettimanale/testostandard").text
                    chiusurasettimanale_traduzioni = info.find("chiusuraSettimanale/traduzioni").getchildren()
                    if (len(chiusurasettimanale_traduzioni)) > 0:
                        for traduzione in chiusurasettimanale_traduzioni:
                            print "%s => %s" % (traduzione.attrib,traduzione.text)
            
            entecompetente = ''
            ruolo_entecompetente = ''
            codice_entecompetente_dbunico20 = ''
            codice_entecompetente_mibac = ''
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
                for contenitore in contenitori:
                    print "%s => %s" % (traduzione.attrib,traduzione.text)
                    #FARE LA INSERT
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
        
            tipo_prenotazioni = ""
            prenotazioni_sitoweb = ""
            prenotazioni_email = ""
            prenotazioni_telefono = ""
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
            nindirizzi = 0
            via_indirizzo_default = ''
            comune_indirizzo_default = ''
            provincia_indirizzo_default = ''
            regione_indirizzo_default = ''
            istat_regione_default = ''
            istat_provincia_default = ''
            istat_comune_default = ''
            localita_indirizzo_default = ''
            cap_indirizzo_default = ''
            latitudine_default = ''
            longitudine_default = ''
            for indirizzo in indirizzi:
                tipo_indirizzo = ""
                if len(indirizzo.attrib) > 0:
                    tipo_indirizzo = indirizzo.attrib[indirizzo.attrib.keys()[0]]
                via_indirizzo = ""
                if (indirizzo.find('via-piazza') != None):
                    via_indirizzo = indirizzo.find('via-piazza').text
                localita_indirizzo = ""
                if (indirizzo.find('localita') != None):
                    localita_indirizzo = indirizzo.find('localita').text
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
                    
                if nindirizzi == 0:
                    via_indirizzo_default = via_indirizzo
                    localita_indirizzo_default = localita_indirizzo
                    comune_indirizzo_default = comune_indirizzo
                    provincia_indirizzo_default = provincia_indirizzo
                    cap_indirizzo_default = cap_indirizzo
                    latitudine_default = latitudine
                    longitudine_default = longitudine             
                nindirizzi += 1
                 
            links = luogodellacultura.find("links")
            if (links):
                for link in links.getchildren():
                    print "%s => %s" % (link.attrib,link.text)
            allegati = luogodellacultura.find("allegati")
            if (allegati):
                for allegato in allegati.getchildren():
                    print "%s => %s" % (allegato.attrib,allegato.text)    

            step += 1
            
            if (longitudine != ""):
                writerow.append(djenc.smart_str(nome))        
                writerow.append(djenc.smart_str(via_indirizzo_default))
                writerow.append(djenc.smart_str(localita_indirizzo_default))
                writerow.append(djenc.smart_str(comune_indirizzo_default))
                writerow.append(djenc.smart_str(provincia_indirizzo_default))
                writerow.append(djenc.smart_str(cap_indirizzo_default))
                writerow.append(djenc.smart_str(sitoweb))
                writerow.append(djenc.smart_str(latitudine_default))
                writerow.append(djenc.smart_str(longitudine_default))
                museiwriter.writerow(writerow)

            print latitudine
            print longitudine
            geom = "GeomFromText('POINT("
            geom += "%f " % (float(longitudine))
            geom += "%f" % (float(latitudine))
            geom += ")', 4326)"
            sql = '''INSERT INTO luoghi (
            codice_dbunico2, stato, nomeRedattore, nomeCapoRedattore, 
            dataValidazione, dataUltimaModifica, datacreazionexml, 
            sorgente, tipologia, categoria, proprieta, nome, descrizione, 
            orario, responsabile, accessibilita, sitoweb,
            email, email_certificata, telefono, chiusurasettimanale,
            entecompetente, ruolo_entecompetente, codice_entecompetente_dbunico20, codice_entecompetente_mibac,
            entegestore, ruolo_entegestore, codice_entegestore_dbunico20, codice_entegestore_mibac, telefono_biglietteria,
            fax_biglietteria, email_biglietteria, costo_biglietto, riduzioni_biglietto, orario_biglietteria,
            tipo_prenotazioni, prenotazioni_sitoweb, prenotazioni_email, prenotazioni_telefono, indirizzo,
            comune, localita, provincia, regione, istat_regione, istat_provincia, istat_comune, cap, latitudine, longitudine,geom)
            ) VALUES (
            '''
            sql += '''%i, '%s', '%s', '%s','%s', '%s', '%s', 
            '%s', '%s','%s', '%s','%s','%s', 
            '%s','%s', '%s','%s',
            '%s', '%s','%s','%s',
            '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');''' % \
            (codice_dbunico2, stato, nomeRedattore, nomeCapoRedattore, dataValidazione, \
            dataUltimaModifica, datacreazionexml, sorgente, tipologiaprevalente, categoriaprevalente, \
            proprieta, nome, descrizione, orario, responsabile, accessibilita, sitoweb,\
            email, email_certificata, telefono, chiusurasettimanale,\
            entecompetente, ruolo_entecompetente, codice_entecompetente_dbunico20, \
            codice_entecompetente_mibac, entegestore, ruolo_entegestore, codice_entegestore_dbunico20, \
            codice_entegestore_mibac, telefono_biglietteria,fax_biglietteria, email_biglietteria, \
            costo_biglietto, riduzioni_biglietto, orario_biglietteria, tipo_prenotazioni, \
            prenotazioni_sitoweb, prenotazioni_email, prenotazioni_telefono, via_indirizzo_default, \
            comune_indirizzo_default, localita_indirizzo_default, provincia_indirizzo_default, \
            regione_indirizzo_default, istat_regione_default, istat_provincia_default, istat_comune_default, \
            cap_indirizzo_default, str(latitudine_default), str(longitudine_default),geom)
            print sql
            cur.execute(sql)
            conn.commit()
conn.close()
quit()


