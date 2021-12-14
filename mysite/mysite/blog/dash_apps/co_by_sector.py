import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
#import dash_bootstrap_components as dbc

k = 0.05
a = 'Fuel combustion in energy industries',
b = 'Fuel combustion in manufacturing industries and construction',
c = 'Transport',
d = 'Industrial processes and product use',
e = 'Agriculture',
f = 'Land use, land use change, and forestry (LULUCF)',
g = 'Waste management'


external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash("co_by_sector", external_stylesheets=external_stylesheet)

df = pd.read_excel(r'C:\Users\User1\Desktop\Blogi\mysiteDjango\mysite\mysite\static\data\european_co2_by_sector_w_indirect.xlsx')

fig = px.line(df, x='Year', y=['Fuel combustion in energy industries', 'Fuel combustion in manufacturing industries and construction',
                               'Transport','Industrial processes and product use','Agriculture','Land use, land use change, and forestry (LULUCF)',
                               'Waste management',],)


app.layout = html.Div(
    dcc.Graph(
        id='fig',
        figure=fig,
        config={'displayModeBar': False},
        style={'width': '100%', 'display': 'inline-block'},
    )

)





