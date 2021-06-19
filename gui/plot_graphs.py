import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from models.initial import db, Country, GDPInfo, PopulationInfo, Emission,Temperature
from peewee import *

# pip install dash -- using conda prompt
# after running script, go to http://127.0.0.1:8050/ on browser
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

emissions = Emission.select().where(Emission.year > 1960)
df_emissions = pd.DataFrame([e for e in emissions.tuples()], columns = ["Index","Country", "Year","Values"])

cumulative_emissions_by_world = Emission.select(fn.SUM(Emission.value).over(Emission.year).alias('cumulativeSum'), Emission.country, Emission.year).where((Emission.year > 1960) & (Emission.country == "World"))
df_cumulative_emissions = pd.DataFrame([e for e in cumulative_emissions_by_world.tuples()], columns = ["CumulativeSum","Country", "Year"])

# TODO: Temperature table should be added.
#mean_temperature_by_country = Temperature.select().where(Temperature.year > 1960)
#df_mean_temperature_by_country = pd.DataFrame([e for e in mean_temperature_by_country.tuples()], columns = ["Index","Country", "Year","Values"])


# to be able to see plotly graphics, we need to download plotly orca package
# conda install -c plotly plotly-orca
fig_cumulative = px.line(df_cumulative_emissions, x="Year", y="CumulativeSum", color="Country",
              line_group="Country", hover_name="Country")


fig_co2 = px.line(df_emissions, x="Year", y="Values", color="Country",
              line_group="Country", hover_name="Country")


app.layout = html.Div(children=[

    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='CO2 Emission and Temperature Analysis'),

        html.Div(children='''
            Cumulative CO2 Emission and Avg.Temperature Correlation
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig_cumulative
        ),
    ], className='row'),

    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children='CO2 Emissions by Country'),

            html.Div(children=''''''),

            dcc.Graph(
                id='graph1',
                figure=fig_co2
            ),
        ], className='six columns'),
        html.Div([
            html.H1(children='Avg. Temperatures by Country'),

            html.Div(children=''''''),

            dcc.Graph(
                id='graph2',
                figure=fig_co2
            ),
        ], className='six columns'),
    ], className='row'),



])


if __name__ == '__main__':
    app.run_server(debug=False)