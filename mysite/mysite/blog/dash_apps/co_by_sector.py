import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objs as go
import dash


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

url = ('https://github.com/attekoskivaara/European-GHG-emissions/blob/main/european_co2_by_sector_w_indirect.xlsx?raw=true')
myfile = requests.get(url)
df = pd.read_excel(myfile.content, engine='openpyxl')

#table_header = [
#    html.Thead(html.Tr([html.Th("2030"), html.Th("2050")]))
#]


html.P(a),
row1 = dcc.Slider(
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

html.P(b),
dcc.Slider(
    id='percentage-slider2',
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
html.P(c),
dcc.Slider(
    id='percentage-slider3',
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
html.P(d),
dcc.Slider(
    id='percentage-slider4',
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
html.P(e),
dcc.Slider(
    id='percentage-slider5',
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
        2: '100%',
    }
),
html.P(f),
dcc.Slider(
    id='percentage-slider6',
    min=0,
    max=3,
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
        2: '100%',
        2.2: '120%',
        2.4: '140%',
        2.6: '160%',
        2.8: '180%',
        3.0: '200%'
    }
),
html.P(g)
dcc.Slider(
    id='percentage-slider7',
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

style = {'width': '33%', 'display': 'inline-block'},

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                id='linechart',
                config={'displayModeBar': False},
                style={'width': '100%', 'display': 'inline-block'},
#        hover_name="Year",
            ), ], className="six columns"),
        html.Div([
            dcc.Graph(
                id='barchart',
                config={'displayModeBar': False},
                style={'width': '100%', 'display': 'inline-block'},
            ), ], className="six columns"),

    ], className="row"),

    html.Div([

        html.Div([
            html.P(a),
            dcc.Input(id='percentage-slider', placeholder="0%", type='number', min=-100, max=200, step=1),
            html.P(b),
            dcc.Input(id='percentage-slider2', placeholder="0%", type='number', min=-100, max=200, step=1),
            html.P(c),
            dcc.Input(id='percentage-slider3', placeholder="0%", type='number', min=-100, max=200, step=1),
            html.P(d),
            dcc.Input(id='percentage-slider4', placeholder="0%", type='number', min=-100, max=200, step=1),
            html.P(e),
            dcc.Input(id='percentage-slider5', placeholder="0%", type='number', min=-100, max=200, step=1),
            html.P(f),
            dcc.Input(id='percentage-slider6', placeholder="0%", type='number', min=-100, max=200, step=1),
            html.P(g),
            dcc.Input(id='percentage-slider7', placeholder="0%", type='number', min=-100, max=200, step=1)

 #       ], className="six columns"),

  #      html.Div([
   #         html.P(b),

    #    ], className="six columns"),

#    ], className="row")

])
        ])
    ])

@app.callback([Output('barchart', 'figure'),
              Output('linechart', 'figure')],
              [Input('percentage-slider', 'value'),
               Input('percentage-slider2', 'value'),
               Input('percentage-slider3', 'value'),
               Input('percentage-slider4', 'value'),
               Input('percentage-slider5', 'value'),
               Input('percentage-slider6', 'value'),
               Input('percentage-slider7', 'value')])
def update_figure(percentage, percentage2, percentage3, percentage4, percentage5, percentage6, percentage7):
    percentage = 0 if percentage is None else percentage
    percentage2 = 0 if percentage2 is None else percentage2
    percentage3 = 0 if percentage3 is None else percentage3
    percentage4 = 0 if percentage4 is None else percentage4
    percentage5 = 0 if percentage5 is None else percentage5
    percentage6 = 0 if percentage6 is None else percentage6
    percentage7 = 0 if percentage7 is None else percentage7

    #-90 totaalipäästöt
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
    df3.iloc[2, 2] *= (percentage)/100+1
    percentage2 = float(percentage2)
    df3.iloc[2, 3] *= percentage2/100+1
    percentage3 = float(percentage3)
    df3.iloc[2, 4] *= percentage3/100+1
    percentage4 = float(percentage4)
    df3.iloc[2, 5] *= percentage4/100+1
    percentage5 = float(percentage5)
    df3.iloc[2, 6] *= percentage5/100+1
    percentage6 = float(percentage6)
    df3.iloc[2, 7] *= percentage6/100+1
    percentage7 = float(percentage7)
    df3.iloc[2, 8] *= percentage7/100+1

    # summataan rivi
    df3['sum'] = df3.drop(['Year', 'Total'], axis=1).sum(axis=1)
    # summataan kolumni (pl. lulucf)
    df3['sum_excl_LULUCF'] = df3.drop(['Year', 'Total', 'Land use, land use change, and forestry (LULUCF)', 'sum'], axis=1).sum(
        axis=1)

    # 2018 päästöt ja lulucf
    q = (df3.iloc[1, 13])

    # lulucf18
    lulucf18 = (df3.iloc[1, 7])
    # -30 ja -50 päästöt huomioiden lulucf
    tot30 = df3.iloc[2, 13]
    tot50 = df3.iloc[3, 13]
    # -30 ja -50 sis. lulucf
    excllulu30 = df3.iloc[2, 14]
    excllulu50 = df3.iloc[3, 14]

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
                    'Change since 1990: %{text:1,.0f}'+'%',
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
                    'Change since 1990: %{text:1,.0f}'+'%',
                    ])
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df1['Year'],
            y=df1['2030 - target (-40%)'],
            mode='markers',
            name='Target - (-40%)',
#            text=df1['2030 - target (-40%)'],
            hovertemplate='Target (-40%) %{y:1,.0f}'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df1['Year'],
            y=df1['2030 - target (-55%)'],
            mode='markers',
            name='Target - (-55%)',
            #            text=df1['2030 - target (-40%)'],
            hovertemplate='Target (-55%) %{y:1,.0f}'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df1['Year'],
            y=df1['2050 - target'],
            mode='markers',
            name='Target - (-100%)',
            #            text=df1['2030 - target (-40%)'],
            hovertemplate='Target (-100%) %{y:1,.0f}'
        )
    )
    fig.update_layout(showlegend = False)
    fig.update_yaxes(title_text='')

    return fig2, fig
