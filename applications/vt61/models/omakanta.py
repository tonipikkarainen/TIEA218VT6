# -*- coding: utf-8 -*-
from gluon.contrib.login_methods.gae_google_account import GaeGoogleAccount
auth.settings.login_form = GaeGoogleAccount()
import datetime

db.define_table('jasen',
  Field('nimi', 'string', required=True,label="Nimi"),
  # Osoite
  Field('osoite', 'string',required=True,label="Osoite"),
  # Label määrää lomakekentän tekstin
  Field('liittymispvm', 'date', required=True, label="Liittymispäivä"),

  Field('syntymavuosi', 'integer', required=True,label="Syntymävuosi")
)


db.define_table('elokuva',
  Field('nimi', 'string', required=True, label="Nimi", unique=True),
  #
  Field('julkaisuvuosi', 'integer',required=True,label="Julkaisuvuosi"),
  # Label määrää lomakekentän tekstin
  Field('vuokrahinta', 'double', required=True, label="Vuokrahinta"),
 
  Field('arvio', 'integer', required=True,label="Arvio"),
  Field('lajityyppiid', 'reference lajityyppi', required=True,label="Lajityyppi")
)

db.define_table('vuokraus',
  Field('jasenid', 'reference jasen', required=True,label="Jäsen"),
  #
  Field('elokuvaid', 'reference elokuva',required=True,label="Elokuva"),
  # Label määrää lomakekentän tekstin
  Field('vuokrauspvm', 'date', required=True,label="Vuokrauspäivämäärä"),
  Field('palautuspvm', 'date', required=False, label="Palautuspäivämäärä")
 
  
)


db.define_table('lajityyppi',
  Field('tyypinnimi', 'string', required=True,label="Lajityyppi")
)

#vaaditaan, että elokuvan lajityyppia vastaava lajityyppi on jo olemassa
db.elokuva.lajityyppiid.requires = IS_IN_DB(db, db.lajityyppi.id, '%(tyypinnimi)s',zero=None)

db.vuokraus.jasenid.requires = IS_IN_DB(db, db.jasen.id, '%(nimi)s',zero=None)
db.vuokraus.elokuvaid.requires = IS_IN_DB(db, db.elokuva.id, '%(nimi)s',zero=None)

db.jasen.liittymispvm.requires = IS_DATE(error_message='Päivämäärä vaaditaan')
#db.vuokraus.palautuspvm.requires = IS_DATE()
#db.vuokraus.vuokrauspvm.requires = IS_DATE(error_message='Vuokrauspäivämäärä on pakollinen')
db.vuokraus.vuokrauspvm.requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'),
                                    minimum=datetime.date(1990,1,1),
                                    error_message='Vuokrauspäivämäärä on pakollinen, pitää olla uudempi kuin 1990-01-01')

db.jasen.nimi.requires = IS_NOT_EMPTY()
db.elokuva.nimi.requires = IS_NOT_EMPTY()












