import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.io as pio
from models.initial import db, Country, GDPInfo, PopulationInfo, Emission

# pip install dash -- using conda prompt
# after running script, go to http://127.0.0.1:8050/ on browser
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

emissions = Emission.select().where(Emission.year > 1960)
df = pd.DataFrame([e for e in emissions.tuples()], columns = ["Index","Country", "Year","Values"])

# to be able to see plotly graphics, we need to download plotly orca package
# conda install -c plotly plotly-orca
fig = px.line(df, x="Year", y="Values", color="Country",
              line_group="Country", hover_name="Country")


app.layout = html.Div(children=[
    html.H1(children='Database Systems Assignment 10'),

    html.Div(children='''
        Visualization for Countries and their CO2 Emission values.
    '''),

    dcc.Graph(
        id='co2-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)