from peewee import Model, SqliteDatabase, CharField, ForeignKeyField, IntegerField, DoubleField

db = SqliteDatabase('./data/db.db')


class BaseModel(Model):
    class Meta:
        database = db


class Country(BaseModel):
    name = CharField(primary_key=True)


class PopulationInfo(BaseModel):
    country = ForeignKeyField(Country, backref='population_infos', column_name='country_name')
    year = IntegerField(null=True)
    count = IntegerField(null=True)


class Emission(BaseModel):
    country = ForeignKeyField(Country, backref='emissions', column_name='country_name')
    year = IntegerField(null=True)
    value = DoubleField(null=True)


class Temperature(BaseModel):
    country = ForeignKeyField(Country, backref='temperatures', column_name='country_name')
    year = IntegerField(null=True)
    value = DoubleField(null=True)


class GDPInfo(BaseModel):
    country = ForeignKeyField(Country, backref='gdp_infos', column_name='country_name')
    year = IntegerField(null=True)
    value = DoubleField(null=True)


