from dataclasses import dataclass
from typing import List, Optional
import pandas as pd

from models.initial import db, Country, GDPInfo, PopulationInfo, Emission

db.drop_tables([Country, GDPInfo, PopulationInfo, Emission])
db.connect(reuse_if_open=True)
db.create_tables([Country, GDPInfo, PopulationInfo, Emission])

into = Optional[int]
floato = Optional[float]


@dataclass
class RawGDPInfo:
    year: into
    value: floato


RawGDPInfos = List[RawGDPInfo]


@dataclass
class RawPopulationInfo:
    year: into
    growth: into
    value: floato


RawPopulationInfos = List[RawPopulationInfo]


@dataclass
class RawEmission:
    year: into
    value: floato


RawEmissions = List[RawEmission]


@dataclass
class RawCountry:
    name: str
    emissions: RawEmissions
    populations: RawPopulationInfos
    gdp: RawGDPInfos


RawCountries = List[RawCountry]


def fill_db(countries: RawCountries):
    for c in countries:
        Country.create(name=c.name)
        for e in c.emissions:
            Emission.create(year=e.year, country=c, value=e.value)
        for g in c.gdp:
            GDPInfo.create(year=g.year, country=c, value=g.value)


def test():
    base_path = '../data/'
    co2_emmision_df = pd.read_csv(base_path + 'co2_emission.csv')
    gdp_df = pd.read_csv(base_path + 'gdp.csv')
    population_growth_df = pd.read_csv(base_path + 'population_growth.csv')
    population_total_df = pd.read_csv(base_path + 'population_total.csv')
    