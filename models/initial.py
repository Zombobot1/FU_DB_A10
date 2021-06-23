from peewee import Model, SqliteDatabase, CharField, ForeignKeyField, IntegerField, DoubleField


db = SqliteDatabase('../data/db.db')


class BaseModel(Model):
    class Meta:
        database = db


class Country(BaseModel):
    name = CharField(unique=True)


class PopulationInfo(BaseModel):
    country = ForeignKeyField(Country, backref='population_infos')
    year = IntegerField(null=True)
    count = IntegerField(null=True)


class Emission(BaseModel):
    country = ForeignKeyField(Country, backref='emissions')
    year = IntegerField(null=True)
    value = DoubleField(null=True)


class Temperature(BaseModel):
    country = ForeignKeyField(Country, backref='temperatures')
    year = IntegerField(null=True)
    value = DoubleField(null=True)


class GDPInfo(BaseModel):
    country = ForeignKeyField(Country, backref='gdp_infos')
    year = IntegerField(null=True)
    value = DoubleField(null=True)


