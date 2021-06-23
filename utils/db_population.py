from dataclasses import dataclass
from typing import List, Optional
import pandas as pd
from collections import defaultdict
import math

from models.initial import db, Country, GDPInfo, PopulationInfo, Emission, Temperature

into = Optional[int]
floato = Optional[float]


@dataclass
class RawInfo:
    year: int
    value: floato

    def __init__(self, year, value):
        self.year = year
        if not math.isnan(value):
            self.value = value
        else:
            self.value = None


RawInfos = List[RawInfo]


@dataclass
class RawCountry:
    name: str
    emissions: RawInfos
    populations: RawInfos
    gdp: RawInfos
    temperatures: RawInfos


RawCountries = List[RawCountry]


def fill_db(countries: RawCountries):
    print('Filling db from raw data')

    for c in countries:
        Country.create(name=c.name)
        for e in c.emissions:
            Emission.create(country=c.name, year=e.year, value=e.value)
        for g in c.gdp:
            GDPInfo.create(country=c.name, year=g.year, value=g.value)
        for p in c.populations:
            PopulationInfo.create(country=c.name, year=p.year, value=p.value)
        for t in c.temperatures:
            Temperature.create(country=c.name, year=t.year, value=t.value)

        print(f'{c.name} inserted')


def co2_emission_df_to_dc(df):
    result = defaultdict(list)
    for i, r in df.iterrows():
        result[r['Entity']].append(RawInfo(r['Year'], r['Annual CO₂ emissions (tonnes )']))
    return result


def extract_years_from_df_row(row, from_=1960, to=2020) -> List[dict]:
    result = []
    for year in range(from_, to + 1):
        if str(year) in row:
            result.append({'year': year, 'value': row[str(year)]})
    return result


def gdp_df_to_dc(df):
    result = defaultdict(list)
    for i, r in df.iterrows():
        for data_point in extract_years_from_df_row(r):
            result[r['Country Name']].append(RawInfo(data_point['year'], data_point['value']))
    return result


def population_df_to_dc(df):
    result = defaultdict(list)
    for i, r in df.iterrows():
        result[r['Country Name']].append(RawInfo(r['Year'], r['Count']))
    return result


def temperature_df_to_dc(df):
    df = df.groupby([' Country', ' Year'])['Temperature - (Celsius)'].median().reset_index()
    result = defaultdict(list)
    for i, r in df.iterrows():
        result[r[' Country']].append(RawInfo(r[' Year'], r['Temperature - (Celsius)']))
    return result


def dfs_to_dc() -> RawCountries:
    print('Converting data frames to raw data')

    base_path = '../data/'
    co2_emission_df = pd.read_csv(base_path + 'co2_emission.csv')
    gdp_df = pd.read_csv(base_path + 'gdp.csv')
    population_total_df = pd.read_csv(base_path + 'population_total.csv')

    t1_df = pd.read_csv(base_path + 'temperature_1961_1990_cl.csv', sep=';')
    t2_df = pd.read_csv(base_path + 'temperature_1991_2020_cl.csv', sep=';')
    t_df = pd.concat([t1_df, t2_df], ignore_index=True, sort=False)
    t_df[' Country'] = t_df[' Country'].str.strip()

    emission = co2_emission_df_to_dc(co2_emission_df)
    gdp = gdp_df_to_dc(gdp_df)
    population = population_df_to_dc(population_total_df)
    temperatures = temperature_df_to_dc(t_df)

    result = []
    for country in emission:
        result.append(RawCountry(country, emission[country], population[country], gdp[country], temperatures[country]))

    print('Data frames were converted successfully')

    return result


def populate_db():
    db.drop_tables([Country, GDPInfo, PopulationInfo, Emission, Temperature])
    db.connect(reuse_if_open=True)
    db.create_tables([Country, GDPInfo, PopulationInfo, Emission, Temperature])

    fill_db(dfs_to_dc())

