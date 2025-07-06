import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import os

# Load telemetry data from CSV
file_path = os.path.join(os.path.dirname(__file__), 'open-telemetry-data.csv')
df = pd.read_csv(file_path)

# Convert timestamps
if 'start_time' in df.columns:
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
if 'end_time' in df.columns:
    df['end_time'] = pd.to_datetime(df['end_time'], unit='ms')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("OpenTelemetry APEX Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H3("Total Events"),
            html.H4(id='total-events')
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.H3("Average Duration (ms)"),
            html.H4(id='avg-duration')
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.H3("Distinct Users"),
            html.H4(id='distinct-users')
        ], style={'width': '30%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='event-type-bar'),
    dcc.Graph(id='events-over-time'),

    html.H3("Raw Telemetry Data"),
    dcc.Dropdown(
        id='event-filter',
        options=[{'label': e, 'value': e} for e in df['event'].dropna().unique()],
        placeholder="Filter by event type",
        multi=True
    ),
    dcc.Graph(id='filtered-table')
])

@app.callback(
    Output('total-events', 'children'),
    Output('avg-duration', 'children'),
    Output('distinct-users', 'children'),
    Input('event-filter', 'value')
)
def update_kpis(event_filter):
    filtered_df = df if not event_filter else df[df['event'].isin(event_filter)]
    return (
        len(filtered_df),
        round(filtered_df['duration'].mean(), 2) if 'duration' in filtered_df.columns else 'N/A',
        filtered_df['user.guid'].nunique() if 'user.guid' in filtered_df.columns else 'N/A'
    )

@app.callback(
    Output('event-type-bar', 'figure'),
    Input('event-filter', 'value')
)
def update_event_bar(event_filter):
    filtered_df = df if not event_filter else df[df['event'].isin(event_filter)]
    event_counts = filtered_df['event'].value_counts().reset_index()
    event_counts.columns = ['event', 'count']
    return px.bar(event_counts, x='event', y='count', title="Events by Type")

@app.callback(
    Output('events-over-time', 'figure'),
    Input('event-filter', 'value')
)
def update_time_series(event_filter):
    filtered_df = df if not event_filter else df[df['event'].isin(event_filter)]
    if 'start_time' not in filtered_df.columns:
        return go.Figure()
    time_data = filtered_df.resample('H', on='start_time').size().reset_index(name='count')
    return px.line(time_data, x='start_time', y='count', title="Events Over Time (Hourly)")

@app.callback(
    Output('filtered-table', 'figure'),
    Input('event-filter', 'value')
)
def update_table(event_filter):
    filtered_df = df if not event_filter else df[df['event'].isin(event_filter)]
    display_df = filtered_df[['event', 'component', 'duration', 'user.guid']].fillna('') \
        if 'component' in filtered_df.columns else filtered_df
    return go.Figure(data=[go.Table(
        header=dict(values=list(display_df.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=[display_df[col] for col in display_df.columns], fill_color='lavender', align='left'))
    ])

app.run_server(debug=True, port=8051)
