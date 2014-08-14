# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 15:20:45 2014

@author: Maurizio Napolitano <napo@fbk.eu>
"""

from pysqlite2 import dbapi2 as sqlite
from datetime import datetime

from sqlalchemy import create_engine, event
from sqlalchemy import Table,Column, Integer, TEXT, ForeignKey, MetaData, DateTime
from geoalchemy import Geometry, GeometryColumn, GeometryDDL
from geoalchemy.spatialite import GeometryExtensionColumn, SQLiteComparator
from sqlalchemy.orm import sessionmaker, mapper


class DBMibac():
    def __init__(self,path,name):   
        dbfile = "sqlite:////%s/%s.sqlite" % (path,name)
        engine = create_engine(dbfile, module=sqlite, echo=False)
        @event.listens_for(engine, "connect")
        def connect(dbapi_connection, connection_rec):
            dbapi_connection.enable_load_extension(True)
            dbapi_connection.execute("SELECT load_extension('mod_spatialite')");
            dbapi_connection.execute("SELECT InitSpatialMetadata();")
            dbapi_connection.text_factory = str
        metadata = MetaData(engine)
        
        self.allegati = Table('allegati', metadata,
            Column('id', Integer, primary_key=True),
            Column('codice_dbunico2', Integer,ForeignKey('luoghicultura.codice_dbunico2')),
            Column('copyright',TEXT, nullable=True),
            Column('url',TEXT, nullable=True),
            Column('ruolo',TEXT, nullable=True),
            Column('didascalia',TEXT, nullable=True),
            Column('mibacidallegato',Integer),
            Column('descrizione',TEXT, nullable=True),
            sqlite_autoincrement=True)
            
        self.extra = Table('extra',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('tipo',TEXT, nullable=True),
            Column('attributo',TEXT, nullable=True),    
            Column('valore',TEXT, nullable=True),
            sqlite_autoincrement=True)

        self.accessibilita = Table('accessibilita',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('chiave',TEXT, nullable=True),
            Column('lingua',TEXT, nullable=True),    
            Column('valore',TEXT, nullable=True),
            sqlite_autoincrement=True)


        self.links = Table('links',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('url',TEXT, nullable=True),
            Column('titolo',TEXT, nullable=True),    
            Column('descrizione',TEXT, nullable=True),
            Column('tipo',TEXT, nullable=True),
            sqlite_autoincrement=True)

        self.indirizzi = Table('indirizzi',metadata,
             Column('id',Integer, primary_key=True,),
             Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
             Column('indirizzo',TEXT, nullable=True),
             Column('cap',TEXT, nullable=True),
             Column('comune',TEXT, nullable=True),
             Column('localita',TEXT, nullable=True),
             Column('provincia',TEXT, nullable=True),
             Column('regione',TEXT, nullable=True),
             Column('latitudine',TEXT, nullable=True),
             Column('longitudine',TEXT, nullable=True),
             Column('istat_comune',TEXT, nullable=True),
             Column('istat_provincia',TEXT, nullable=True),
             Column('istat_regione',TEXT, nullable=True),
             GeometryExtensionColumn('geom', Geometry(2)))


        self.luoghicultura= Table('luoghicultura',metadata,
           #Column('mibacxml',TEXT, nullable=False),
            Column('cap',TEXT),
            Column('categoria',TEXT),
            Column('chiusurasettimanale',TEXT), 
            Column('created',DateTime, default=datetime.now()),    
            Column('codice_dbunico2',Integer, primary_key=True),
            Column('codice_entecompetente_dbunico20',TEXT),     
            Column('codice_entecompetente_mibac',TEXT),     
            Column('codice_entegestore_dbunico20',TEXT),     
            Column('codice_entegestore_mibac',TEXT),    
            Column('comune',TEXT),    
            Column('costo_biglietto',TEXT),
            Column('data_validazione',TEXT),
            Column('data_ultima_modifica',TEXT),  
            Column('data_creazione_xml',TEXT),
            Column('descrizione',TEXT),
            Column('email',TEXT),     
            Column('email_biglietteria',TEXT),     
            Column('email_certificata',TEXT),   
            Column('entecompetente',TEXT),     
            Column('entecompilatore',TEXT),     
            Column('entegestore',TEXT),     
            Column('fax',TEXT),     
            Column('fax_biglietteria',TEXT),     
            Column('idtipologialuogo',Integer),  
            Column('img',TEXT),     
            Column('indirizzo',TEXT),     
            Column('istat_regione',TEXT),
            Column('istat_provincia',TEXT),
            Column('istat_comune',TEXT),
            Column('latitudine',TEXT),   
            Column('localita',TEXT),   
            Column('longitudine',TEXT),   
            Column('nome_redattore',TEXT),   
            Column('nome_capo_redattore',TEXT),   
            Column('nome',TEXT),   
            Column('orario',TEXT),   
            Column('orario_biglietteria',TEXT),     
            Column('prenotazioni_sitoweb',TEXT),   
            Column('prenotazioni_email',TEXT),   
            Column('prenotazioni_telefono',TEXT),   
            Column('proprieta',TEXT),   
            Column('provincia',TEXT),     
            Column('responsabile',TEXT),   
            Column('regione',TEXT),   
            Column('riduzioni_biglietto',TEXT),     
            Column('ruolo_entecompetente',TEXT),   
            Column('ruolo_entegestore',TEXT),   
            Column('stato',TEXT),   
            Column('sitoweb',TEXT),   
            Column('sorgente',TEXT),   
            Column('telefono',TEXT),   
            Column('telefono_biglietteria',TEXT),   
            Column('tipologialuogo',TEXT),   
            Column('tipologia',TEXT),   
            Column('tipo_prenotazioni',TEXT),   
            Column('riduzioni_biglietto',TEXT),   
            GeometryExtensionColumn('geom', Geometry(2)))
            
        mapper(Allegati, self.allegati)
        mapper(Extra,self.extra)
        mapper(Links,self.links)
        mapper(Indirizzi, self.indirizzi, properties={
        'geom': GeometryColumn(self.indirizzi.c.geom,
        comparator=SQLiteComparator)}) 
        mapper(LuoghiCultura, self.luoghicultura, properties={
        'geom': GeometryColumn(self.luoghicultura.c.geom,
        comparator=SQLiteComparator)}) 
        GeometryDDL(self.indirizzi)
        GeometryDDL(self.luoghicultura)
        metadata.drop_all()
        metadata.create_all()
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def add(self,indata):
        self.session.add(indata)
        
class Allegati(object):
    def __init__(self, codice_dbunico2, copyright, url, ruolo, didascalia,mibacidallegato,descrizione):   
        self.codice_dbunico2 = codice_dbunico2
        self.copyright = copyright
        self.url = url
        self.ruolo = ruolo
        self.didascalia = didascalia
        self.mibacidallegato = mibacidallegato

class Extra(object):
    def __init__(self,codice_dbunico2, tipo, attributo, valore):   
        self.codice_dbunico2 = codice_dbunico2
        self.tipo = tipo   
        self.attributo = attributo
        self.valore = valore
         
class Links(object):
    def __init__(self,codice_dbunico2,url,titolo,descrizione,tipo):
        self.id = id        
        self.codice_dbunico2 = codice_dbunico2
        self.url = url
        self.titolo = titolo 
        self.descrizione = descrizione 
        self.tipo = tipo 

class Indirizzi(object):
    def __init__(self, codice_dbunico2, indirizzo, cap, comune, localita, provincia, 
                 regione, latitudine, longitudine, istat_comune, istat_provincia, istat_regione, geom):
        self.codice_dbunico2 = codice_dbunico2
        self.indirizzo = indirizzo
        self.cap = cap
        self.comune = comune
        self.localita = localita
        self.provincia = provincia
        self.regione = regione
        self.latitudine = latitudine
        self.longitudine = longitudine
        self.istat_comune = istat_comune
        self.istat_provincia = istat_provincia
        self.istat_regione = istat_regione
        self.geom = geom

class LuoghiCultura(object):
    def __init__(self, cap,categoria,chiusurasettimanale,
        codice_dbunico2, codice_entecompetente_dbunico20,codice_entecompetente_mibac,
        codice_entegestore_dbunico20,codice_entegestore_mibac,
        comune,costo_biglietto,data_validazione,data_ultima_modifica,
        data_creazione_xml,descrizione, email, email_biglietteria,
        email_certificata, entecompetente,entecompilatore,entegestore,fax,
        fax_biglietteria,idtipologialuogo, img,indirizzo, istat_regione,
        istat_provincia,istat_comune, latitudine,localita, longitudine,
        nome_redattore,nome_capo_redattore, nome, orario,  
        orario_biglietteria, prenotazioni_sitoweb,prenotazioni_email,  
        prenotazioni_telefono, proprieta, provincia,responsabile,   
        regione, riduzioni_biglietto, ruolo_entecompetente,   
        ruolo_entegestore, stato, sitoweb, sorgente, telefono,
        telefono_biglietteria, tipologia,tipologialuogo, tipo_prenotazioni,geom):
        #self.mibacxml = mibacxml
        self.cap = cap
        self.categoria = categoria
        self.chiusurasettimanale  = chiusurasettimanale 
        self.created = datetime.now()    
        self.codice_dbunico2 = codice_dbunico2
        self.codice_entecompetente_dbunico20 = codice_entecompetente_dbunico20     
        self.codice_entecompetente_mibac = codice_entecompetente_mibac     
        self.codice_entegestore_dbunico20 = codice_entegestore_dbunico20    
        self.codice_entegestore_mibac = codice_entegestore_mibac     
        self.comune = comune
        self.costo_biglietto =  costo_biglietto    
        self.data_validazione = data_validazione
        self.data_ultima_modifica = data_ultima_modifica  
        self.data_creazione_xml = data_creazione_xml
        self.descrizione = descrizione        
        self.email = email
        self.email_biglietteria = email_biglietteria    
        self.email_certificata = email_certificata    
        self.entecompetente = entecompetente    
        self.entecompilatore = entecompilatore 
        self.entegestore = entegestore  
        self.fax = fax  
        self.fax_biglietteria =  fax_biglietteria    
        self.idtipologialuogo = idtipologialuogo  
        self.img = img
        self.indirizzo = indirizzo
        self.istat_regione = istat_regione
        self.istat_provincia = istat_provincia
        self.istat_comune = istat_comune
        self.latitudine =latitudine    
        self.localita = localita   
        self.longitudine =longitudine
        self.nome_redattore =nome_redattore
        self.nome_capo_redattore =nome_capo_redattore
        self.nome = nome
        self.orario =  orario  
        self.orario_biglietteria =  orario_biglietteria    
        self.prenotazioni_sitoweb = prenotazioni_sitoweb   
        self.prenotazioni_email =  prenotazioni_email  
        self.prenotazioni_telefono =  prenotazioni_telefono  
        self.proprieta = proprieta   
        self.provincia = provincia     
        self.responsabile = responsabile   
        self.regione = regione  
        self.riduzioni_biglietto = riduzioni_biglietto    
        self.ruolo_entecompetente = ruolo_entecompetente   
        self.ruolo_entegestore = ruolo_entegestore   
        self.stato = stato   
        self.sitoweb = sitoweb   
        self.sorgente = sorgente   
        self.telefono = telefono
        self.telefono_biglietteria = telefono_biglietteria   
        self.tipologialuogo = tipologialuogo   
        self.tipologia = tipologia   
        self.tipo_prenotazioni = tipo_prenotazioni 
        self.geom = geom




