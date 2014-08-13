# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 15:20:45 2014

@author: Maurizio Napolitano <napo@fbk.eu>
"""
#from sqlalchemy import *
#from sqlalchemy.orm import *
#from pysqlite2 import dbapi2 as sqlite
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import create_engine
from datetime import datetime
#from pyspatialite import dbapi2 as db
#from managexmlmibac import *
#import tempfile as tmp
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,Column, DateTime, Integer, String, ForeignKey, MetaData
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy.orm import sessionmaker, mapper
#
#tmpdb = tmp.mkstemp()
#print tmpdb
#dbfile = "sqlite:////%s" % tmpdb[1]  
#engine = create_engine('sqlite:///:memory:', echo=True)
#Base = declarative_base()
#engine = create_engine(dbfile, module=sqlite, echo=True)
#metadata = MetaData(engine)
#Base = declarative_base(metadata=MetaData(engine))   
#Base.metadata.create_all(engine) 
#connection = engine.raw_connection().connection
#connection.enable_load_extension(True)        
#Session = sessionmaker(bind=engine)
#session = Session()
#session.execute("SELECT load_extension('mod_spatialite');")
#session.execute("SELECT InitSpatialMetadata();")  
#GeometryDDL(Luoghi.__table__) 

class DBMibac():
    def __init__(self,path,name):   
        dbfile = "sqlite:////%s/%s.sqlite" % (path,name)
        engine = create_engine(dbfile, echo=True)
        metadata = MetaData(engine)
        #Base = declarative_base(metadata=metadata)
        #,ForeignKey('luoghicultura.codice_dbunico2')),\,sqlite_autoincrement=True
        self.allegati = Table('allegati', metadata,
            Column('id', Integer, primary_key=True),
            Column('codice_dbunico2', Integer,ForeignKey('luoghicultura.codice_dbunico2')),
            Column('copyright',String, nullable=True),
            Column('url',String, nullable=True),
            Column('ruolo',String, nullable=True),
            Column('didascalia',String, nullable=True),
            Column('mibacallegato',Integer),
            Column('descrizione',String, nullable=True))
            
        self.traduzioni = Table('traduzioni',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('chiave',String, nullable=True),
            Column('lingua',String, nullable=True),    
            Column('valore',String, nullable=True))

        self.altro = Table('altro',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('chiave',String, nullable=True),
            Column('lingua',String, nullable=True),    
            Column('valore',String, nullable=True))

        self.accessibilita = Table('accessibilita',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('chiave',String, nullable=True),
            Column('lingua',String, nullable=True),    
            Column('valore',String, nullable=True))

        self.links = Table('links',metadata,
            Column('id',Integer, primary_key=True,),
            Column('codice_dbunico2',Integer,ForeignKey('luoghicultura.codice_dbunico2')), 
            Column('chiave',String, nullable=True),
            Column('lingua',String, nullable=True),    
            Column('valore',String, nullable=True))

        self.luoghicultura= Table('luoghicultura',metadata,
            Column('mibacxml',String, nullable=False),
            Column('cap',String),
            Column('categoria',String),
            Column('chiusurasettimanale',String), 
            Column('created',DateTime, default=datetime.now()),    
            Column('codice_dbunico2',Integer, primary_key=True),
            Column('codice_entecompetente_dbunico20',String),     
            Column('codice_entecompetente_mibac',String),     
            Column('codice_entegestore_dbunico20',String),     
            Column('codice_entegestore_mibac',String),    
            Column('comune',String),    
            Column('costo_biglietto',String),
            Column('data_validazione',DateTime),
            Column('data_ultima_modifica',DateTime),  
            Column('data_creazione_xml',DateTime),
            Column('descrizione',String),
            Column('email',String),     
            Column('email_biglietteria',String),     
            Column('email_certificata',String),   
            Column('entecompetente',String),     
            Column('entecompilatore',String),     
            Column('entegestore',String),     
            Column('fax',String),     
            Column('fax_biglietteria',String),     
            Column('idtipologialuogo',Integer),  
            Column('img',String),     
            Column('indirizzo',String),     
            Column('istat_regione',Integer),
            Column('istat_provincia',Integer),
            Column('istat_comune',Integer),
            Column('latitudine',String),   
            Column('localita',String),   
            Column('longitudine',String),   
            Column('nome_redattore',String),   
            Column('nome_capo_redattore',String),   
            Column('nome',String),   
            Column('orario',String),   
            Column('orario_biglietteria',String),     
            Column('prenotazioni_sitoweb',String),   
            Column('prenotazioni_email',String),   
            Column('prenotazioni_telefono',String),   
            Column('proprieta',String),   
            Column('provincia',String),     
            Column('responsabile',String),   
            Column('regione',String),   
            Column('riduzioni_biglietto',String),     
            Column('ruolo_entecompetente',String),   
            Column('ruolo_entegestore',String),   
            Column('stato',String),   
            Column('sitoweb',String),   
            Column('sorgente',String),   
            Column('telefono',String),   
            Column('telefono_biglietteria',String),   
            Column('tipologialuogo',String),   
            Column('tipologia',String),   
            Column('tipo_prenotazioni',String),   
            Column('riduzioni_biglietto',String))   
           # Column('geom',GeometryColumn(Point(2))))
            
        mapper(Allegati, self.allegati)
        mapper(Traduzioni, self.traduzioni)
        mapper(Altro,self.altro)
        mapper(Accessibilita,self.accessibilita)
        mapper(Links,self.links)
        mapper(LuoghiCultura,self.luoghicultura)
        self.connection = engine.connect()#engine.raw_connection().connection
        #self.connection.enable_load_extension(True)
        metadata.drop_all()
        metadata.create_all()
        Session = sessionmaker(bind=engine)
        self.session = Session()
#        self.session.execute("SELECT load_extension('mod_spatialite');")
#        self.session.execute("SELECT InitSpatialMetadata();")
        #GeometryDDL(LuoghiCultura.__table__)
    def add(self,indata):
        self.session.add(indata)
        
class Allegati(object):
    def __init__(self, id,codice_dbunico2, copyright, url, ruolo, didascalia,mibacallegato,descrizione):
        self.id = id        
        self.codice_dbunico2 = codice_dbunico2
        self.copyright = copyright
        self.url = url
        self.ruolo = ruolo
        self.didascalia = didascalia
        self.mibacallegato = mibacallegato

class Traduzioni(object):
    def __init__(self, id,codice_dbunico2, chiave, lingua, valore):
        self.id = id        
        self.codice_dbunico2 = codice_dbunico2
        self.lingua = lingua
        self.valore = valore

class Altro(object):
    def __init__(self, id,codice_dbunico2, chiave, lingua, valore):
        self.id = id        
        self.codice_dbunico2 = codice_dbunico2
        self.lingua = lingua
        self.valore = valore   

class Accessibilita(object):
    def __init__(self, id,codice_dbunico2, chiave, lingua, valore):
        self.id = id        
        self.codice_dbunico2 = codice_dbunico2
        self.lingua = lingua
        self.valore = valore  
        
class Links(object):
    def __init__(self, id,codice_dbunico2, chiave, lingua, valore):
        self.id = id        
        self.codice_dbunico2 = codice_dbunico2
        self.lingua = lingua
        self.valore = valore 

class LuoghiCultura(object):
    def __init__(self, mibacxml,cap,categoria,chiusurasettimanale,
        codice_dbunico20, codice_entecompetente_dbunico20,codice_entecompetente_mibac,
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
        self.mibacxml = mibacxml
        self.cap = cap
        self.categoria = categoria
        self.chiusurasettimanale  = chiusurasettimanale 
        self.created = datetime.now()    
        self.codice_dbunico20 = codice_dbunico20
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
        #self.geom = geom

 
#class LuoghiCultura(DBMibac.Base):
#    __tablename__ = 'luoghicultura'
#    mibacxml = Column(String, nullable=False)
#    cap = Column(String)
#    categoria = Column(String)
#    chiusurasettimanale  = Column(String) 
#    created = Column(DateTime, default=datetime.now())    
#    codice_dbunico2 = Column(Integer, primary_key=True)
#    codice_entecompetente_dbunico20 = Column(String)     
#    codice_entecompetente_mibac = Column(String)     
#    codice_entegestore_dbunico20 = Column(String)     
#    codice_entegestore_mibac = Column(String)     
#    comune = Column(String)     
#    costo_biglietto = Column(String)     
#    data_validazione = Column(DateTime)
#    data_ultima_modifica = Column(DateTime)  
#    data_creazione_xml = Column(DateTime)
#    descrizione = Column(String)        
#    email = Column(String)     
#    email_biglietteria = Column(String)     
#    email_certificata = Column(String)     
#    entecompetente = Column(String)     
#    enteCompilatore = Column(String)     
#    entegestore = Column(String)     
#    fax = Column(String)     
#    fax_biglietteria = Column(String)     
#    idtipologialuogo = Column(Integer)  
#    img = Column(String)     
#    indirizzo = Column(String)     
#    istat_regione = Column(Integer)
#    istat_provincia = Column(Integer)
#    istat_comune = Column(Integer)
#    latitudine = Column(String)   
#    localita = Column(String)   
#    longitudine = Column(String)   
#    nome_redattore = Column(String)   
#    nome_capo_redattore = Column(String)   
#    nome = Column(String)   
#    orario = Column(String)   
#    orario_biglietteria = Column(String)     
#    prenotazioni_sitoweb = Column(String)   
#    prenotazioni_email = Column(String)   
#    prenotazioni_telefono = Column(String)   
#    proprieta = Column(String)   
#    provincia = Column(String)     
#    responsabile = Column(String)   
#    regione = Column(String)   
#    riduzioni_biglietto = Column(String)     
#    ruolo_entecompetente = Column(String)   
#    ruolo_entegestore = Column(String)   
#    stato = Column(String)   
#    sitoweb = Column(String)   
#    sorgente = Column(String)   
#    telefono = Column(String)   
#    telefono_biglietteria = Column(String)   
#    tipologialuogo = Column(String)   
#    tipologia = Column(String)   
#    tipo_prenotazioni = Column(String)   
#    riduzioni_biglietto = Column(String)   
#    geom = GeometryColumn(Point(2))



