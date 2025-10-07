from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import sqlite3
import os
from django_plotly_dash import DjangoDash
from pathlib import Path
import dash_html_components as html
from datetime import timedelta
import re
from gear_app.models import Equipment
from django_plotly_dash import DjangoDash
import pymysql
from dash import Input, Output

# Luo Dash-sovellus
app = DjangoDash("gear_dash", serve_locally=True)

def serve_layout():
    # Yhdistä SQLite-tietokantaan

    # 1) MySQL-yhteys
    conn = pymysql.connect(
        host='hulicupter.mysql.pythonanywhere-services.com',
        user='hulicupter',
        password='siemensM55!',
        database='hulicupter$default',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    query = """
    SELECT
        e.id,
        CONCAT(e.brand, ' ', e.model) AS Equipment,
        s.name AS Sport,
        et.name AS Type,
        COALESCE(a.distance, 0) AS "Total Distance (km)",
        COALESCE(a.duration, 0) AS "Raw Duration",
        COALESCE(a.moving_time, 0) AS "Moving Time",
        COALESCE(a.average_speed, 0) AS "Average Speed"
    FROM
        activities_app_activity a
    JOIN
        activities_app_activity_gears ag ON a.id = ag.activity_id
    JOIN
        gear_app_equipment e ON ag.equipment_id = e.id
    LEFT JOIN
        gear_app_sport s ON e.sport_id = s.id
    LEFT JOIN
        gear_app_equipmenttype et ON e.equipment_type_id = et.id
    """



 #   df = pd.read_sql_query(query, conn)
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    df = pd.DataFrame(rows)

    conn.close()


    # Pakota numeeriseksi
    num_cols = ['Total Distance (km)', 'Raw Duration', 'Moving Time', 'Average Speed']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    '''
    # Hae default uses ORM:llä
    equipment_default_uses = {
        eq.id: ", ".join(s.name for s in eq.default_uses.all())
        for eq in Equipment.objects.all()
    }
    df["Default Uses"] = df["id"].map(equipment_default_uses)
    '''
    # Lisää muokattu sarake ja aggregoi
    df['Total Moving Time (hours)'] = (df['Moving Time'] / (1_000_000 * 3600)).round(1)


    usage_counts = df.groupby('Equipment')['Total Distance (km)'].count().reset_index(name='Usage Count')
    df = df.drop(columns=['Moving Time'])

    summary_df = df.groupby('Equipment', as_index=False).agg({
        'Equipment': 'first',
        'Sport': 'first',
        'Type': 'first',
        'Total Moving Time (hours)': 'sum',
        'Total Distance (km)': 'sum',
    })
    # Liitä summary_df:ään
    summary_df = summary_df.merge(usage_counts, on='Equipment', how='left')

    print("nimet")
    print(summary_df.columns.tolist())
    print(summary_df["Total Moving Time (hours)"].tolist())
    # Nimeä sarakkeet fiksusti
    #summary_df = summary_df.rename(columns={
    #    'duration_timedelta': 'Total Duration (hours)',
    #}).reset_index()

    sporty_colors = {
    'Equipment 1': '#1f77b4',  # Dark Blue
    'Equipment 2': '#ff4136',  # Strong Red
    'Equipment 3': '#2ca02c',  # Sporty Green
    'Equipment 4': '#7f7f7f'   # Neutral Gray
    }


    # Kuvaaja oikeasta datasta
    fig = px.bar(
        summary_df,
        x='Equipment',
        y='Total Distance (km)',
        color='Equipment',
        hover_data=['Total Distance (km)'],
        title='Total Distance',
        color_discrete_map=sporty_colors
    )

    # Layout ilman funktiota
    return html.Div([
        html.H2("My Gear"),

        dash_table.DataTable(
            data=summary_df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in summary_df.columns],
            filter_action="native",
            sort_action="native",
            page_size=10,
            style_table={
                'overflowX': 'auto',
                'maxHeight': 'auto',
                'overflowY': 'auto'
            },
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
        ),

        html.H2("Gear Usage Chart"),
        dcc.Graph(figure=fig),

    #    html.Br(),
    #    html.A("➕ Add New Gear", href="/gear_app/equipment_form", target="_blank"),
    #    html.Br(),
    #    html.A("⬅️ Back to Dashboard", href="/user_app/user", target="_blank"),
        html.Br(),
        html.A("Login", href="/user_app/login", target="_blank")

    ], style={
        'width': '100%',
        'maxWidth': '1200px',
        'height': '100%',
        'maxHeight': 'none',
        'overflow': 'visible',
        'paddingBottom': '50px'
    })


app.layout = serve_layout


@app.callback(
    Output('gear-graph', 'figure'),
    Input('gear-table', 'data')  # ← this gives the filtered data
)
def update_figure(filtered_data):
    if not filtered_data:
        return px.bar(title="No data")

    filtered_df = pd.DataFrame(filtered_data)

    # You can use the same color map and hover data
    fig = px.bar(
        filtered_df,
        x='Equipment',
        y='Total Distance (km)',
        color='Equipment',
        hover_data=['Total Distance (km)'],
        title='Total Distance (Filtered)',
        color_discrete_map=sporty_colors
    )

    return fig
