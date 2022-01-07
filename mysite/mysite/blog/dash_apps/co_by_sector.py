import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
#import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objs as go

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



app.layout = html.Div([
    dcc.Graph(
        id='linechart',
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
    ),

    dash_table.DataTable(
        id = 'table',
        columns = [{"name": i, "id": i} for i in df.columns],
        data = df.to_dict('records'),)

])


@app.callback([Output('barchart', 'figure'),
              Output('linechart', 'figure')],
              [Input('percentage-slider', 'value')])
def update_figure(percentage):
    tot90 = df.at[0, 'Total']

    #tehdään df2 barchartteihein

    df2 = df.loc[(df['Year'] == 1990) | (df['Year'] == 2018)]
    df30 = df.loc[(df['Year'] == 2018)]
#    df30 = df30.drop(['2050 - target', '2030 - target (-40%)', '2030 - target (-55%)', 'Total', '% change', '2050 target change', '2nd target change', '1st target change'], axis=1)
#    df2 = df2.drop(['2050 - target', '2030 - target (-40%)', '2030 - target (-55%)', 'Total', '% change', '2050 target change', '2nd target change', '1st target change'], axis=1)
    df30 = df30.replace(2018, 2030)
    df50 = df30.replace(2030, 2050)
    df2 = df2.append(df30)
    df2 = df2.append(df50)
    df2 = df2.reset_index(drop=True)

    df1 = df.copy()
    df3 = df2.copy()
    percentage = float(percentage)
    df3.iloc[2, 2] *= percentage

    # summataan kolumni
    df3['sum'] = df3.drop(['Year'], axis=1).sum(axis=1)
    # summataan kolumni (pl. lulucf)
    df3['sum_excl_LULUCF'] = df3.drop(['Year', 'Land use, land use change, and forestry (LULUCF)', 'sum'], axis=1).sum(
        axis=1)
    # 2018 päästöt ja lulucf
    q = (df3.iloc[1, 14])

    # lulucf18
    lulucf18 = (df3.iloc[1, 6])
    # -30 ja -50 päästöt miinus lulucf
    tot30 = df3.iloc[2, 9]
    tot50 = df3.iloc[3, 9]
    # -30 ja -50 sis. lulucf
    excllulu30 = df3.iloc[2, 10]
    excllulu50 = df3.iloc[3, 10]

    df1.loc[df1.Year == 2050, 'Estimate'] = tot50
    df1.loc[df1.Year == 2030, 'Estimate'] = tot30
    df1.loc[df1.Year == 2030, 'Estimate excl. LULUCF'] = excllulu30
    df1.loc[df1.Year == 2050, 'Estimate excl. LULUCF'] = excllulu50

    df1.loc[df1.Year == 2018, 'Estimate'] = q
    df1.loc[df1.Year == 2018, 'Estimate excl. LULUCF'] = q - lulucf18

    lulucf30 = tot30 - excllulu30
    lulucf50 = tot50 - excllulu50

    df1.loc[df1.Year == 2018, 'LULUCF'] = lulucf18
    df1.loc[df1.Year == 2030, 'LULUCF'] = lulucf30
    df1.loc[df1.Year == 2050, 'LULUCF'] = lulucf50

    df1['% change to 30'] = (df1['Estimate'] - tot90) / tot90 * 100
    df1['% change to 30 incl. lulucf'] = (df1['Estimate excl. LULUCF'] - tot90) / tot90 * 100

    fig2 = px.bar(df3, x='Year', y=['Fuel combustion in energy industries', 'Fuel combustion in manufacturing industries and construction','Transport','Industrial processes and product use','Agriculture','Land use, land use change, and forestry (LULUCF)','Waste management',
                                    'Indirect GHG emissions'],)

    fig2.update_xaxes(
        dict(type="category"),
        title='',
        #        title_font=(dict(size=18)),
        title_standoff=10,
        linecolor='darkgray',
    )

    fig = px.line(df1, x='Year', y=['Total', 'Land use, land use change, and forestry (LULUCF)'])

    fig.add_trace(
        go.Scatter(
            x=df1['Year'],
            y=df1['Estimate excl. LULUCF'],
            mode='lines+markers',
            connectgaps=True,
            name='GHG estimate',
            line=dict(dash='dash', color='#907163'),
            text=df1['% change to 30 incl. lulucf'],
            hovertemplate="<br>".join([
                    '%{y:1,.0f}',
                    'Change since 1990: %{text:1,.1f}'+'%',
                    ])
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df1['Year'],
            y=df1['Estimate'],
            mode='lines+markers',
            connectgaps=True,
            name='GHG estimate incl. LULUCF',
            line=dict(dash='dash', color='#907163'),
            text=df1['% change to 30'],
            hovertemplate="<br>".join([
                    '%{y:1,.0f}',
                    'Change since 1990: %{text:1,.1f}'+'%',
                    ])
        )
    )

    return fig2, fig






