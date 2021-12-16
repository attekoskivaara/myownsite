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

fig = px.line(df, x='Year', y=['Total', 'Land use, land use change, and forestry (LULUCF)'],)


app.layout = html.Div([
    dcc.Graph(
        id='linechart',
        figure=fig,
        config={'displayModeBar': False},
        style={'width': '100%', 'display': 'inline-block'},
#        hover_name="Year",
    ),
    dcc.Graph(
        id='barchart',
        config={'displayModeBar': False},
        style={'width': '100%', 'display': 'inline-block'},

    ),

    dcc.Slider(
        id='percentage-slider',
        min=0,
        max=2,
        step=0.1,
        value=1,
        marks={
            0: '-100%',
            0.2: '-80%',
            0.4: '-60%',
            0.6: '-40%',
            0.8: '-20%',
            1: '0%',
            1.2: '+20%',
            1.4: '+40%',
            1.6: '60%',
            1.8: '80%',
            2: '100%'
        }
    )])

@app.callback(
    Output('barchart', 'figure'),
    [Input('percentage-slider', 'value')])
def update_figure(percentage):
    df2 = df.loc[(df['Year'] == 1990) | (df['Year'] == 2018)]
    df30 = df.loc[(df['Year'] == 2018)]
#    df30 = df30.drop(['2050 - target', '2030 - target (-40%)', '2030 - target (-55%)', 'Total', '% change', '2050 target change', '2nd target change', '1st target change'], axis=1)
#    df2 = df2.drop(['2050 - target', '2030 - target (-40%)', '2030 - target (-55%)', 'Total', '% change', '2050 target change', '2nd target change', '1st target change'], axis=1)
    df30 = df30.replace(2018, 2030)
    df50 = df30.replace(2030, 2050)
    df2 = df2.append(df30)
    df2 = df2.append(df50)
    df2 = df2.reset_index(drop=True)

    df3 = df2.copy()
    percentage = float(percentage)
    df3.iloc[2, 2] *= percentage


    fig2 = px.bar(df3, x='Year', y=['Fuel combustion in energy industries', 'Fuel combustion in manufacturing industries and construction','Transport','Industrial processes and product use','Agriculture','Land use, land use change, and forestry (LULUCF)','Waste management',
                                    'Indirect GHG emissions'],)

    fig2.update_xaxes(
        dict(type="category"),
        title='',
        #        title_font=(dict(size=18)),
        title_standoff=10,
        linecolor='darkgray',

    )
    return fig2






