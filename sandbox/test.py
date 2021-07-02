from peewee import sqlite3

from models.initial import db, Country, GDPInfo, PopulationInfo, Emission, Temperature
from utils.db_population import populate_db

populate_db()

# db.drop_tables([Country, GDPInfo, PopulationInfo, Emission, Temperature])
# db.connect(reuse_if_open=True)
# db.create_tables([Country, GDPInfo, PopulationInfo, Emission, Temperature])
#
# country = Country.create(name='Iraq')
# Emission.create(country=country, year=1999, value=1.1)