import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from models.initial import db, Country, GDPInfo, PopulationInfo, Emission,Temperature
from peewee import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

def select_all_tasks(file, q):
    conn = create_connection(file)
    cur = conn.cursor()
    cur.execute(q)
    rows = cur.fetchall()
    return rows


q = 'SELECT SUM("t1"."value")  AS "cumulativeSum", "t1"."year" AS "year" FROM "emission" AS "t1" WHERE (("t1"."year" > 1961) AND ("t1"."country_name" = "World")) GROUP BY "year"'
path = "./data/db.db"
res = select_all_tasks(path,q)


# to be able to see plotly graphics, we need to download plotly orca package
# conda install -c plotly plotly-orca
# pip install dash -- using conda prompt
# after running script, go to http://127.0.0.1:8050/ on browser

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_cumulative_emissions = pd.DataFrame(res, columns = ["CumulativeSum", "Year"])

df_emissions = emissions = Emission.select().where(Emission.year >= 1961)
df_emissions = pd.DataFrame([e for e in emissions.tuples()], columns = ["Index","Country", "Year","Values"])


mean_temperature_by_country = Temperature.select(fn.AVG(Temperature.value).alias('avgTemp'), Temperature.year).where(Temperature.year >= 1961).group_by(Temperature.year)
df_mean_temperature_by_country = pd.DataFrame([e for e in mean_temperature_by_country.tuples()], columns = ["AvgTemp", "Year"])


temperature_by_country = Temperature.select(Temperature.value, Temperature.year, Temperature.country).where(Temperature.year >= 1961)
df_temperature_by_country = pd.DataFrame([e for e in temperature_by_country.tuples()], columns = ["Values", "Year", "Country"])

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df_cumulative_emissions.iloc[:,1], y=df_cumulative_emissions.iloc[:,0], name="Cumulative CO2"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df_mean_temperature_by_country.iloc[:,1], y=df_mean_temperature_by_country.iloc[:,0], name="Average Temperature"),
    secondary_y=True,
)

# Set x-axis title
fig.update_xaxes(title_text="Year")

# Set y-axes titles
fig.update_yaxes(title_text="Avg. Tempeature", secondary_y=True)
fig.update_yaxes(title_text="Cumulative CO2", secondary_y=False)
fig.update_layout(
    xaxis=dict(
        rangeslider=dict(
            visible=True
        )
    )
)
fig.show()

## Figure - Yearly Temperature
fig_temp = px.line(df_temperature_by_country, x="Year", y="Values", color="Country",
              line_group="Country", hover_name="Country")

## Figure - Yearly CO2
fig_co2 = px.line(df_emissions, x="Year", y="Values", color="Country",
              line_group="Country", hover_name="Country")

#HTML Layout
app.layout = html.Div(children=[

    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='CO2 Emission and Temperature Analysis'),

        html.Div(children='''
            Cumulative CO2 Emission and Avg.Temperature Correlation
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig
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
            html.H1(children='Yearly Temperatures by Country'),

            html.Div(children=''''''),

            dcc.Graph(
                id='graph2',
                figure=fig_temp
            ),
        ], className='six columns'),
    ], className='row'),

])

def main():
    app.run_server(debug=False,
                  port=8000, host='127.0.0.1')

#if __name__ == '__main__':
#    app.run_server(debug=False,
#                  port=8050)