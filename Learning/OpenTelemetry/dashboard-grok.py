import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import re
from datetime import datetime
import os

# Initializing the Dash app
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])

# Reading and parsing the CSV file
def load_and_parse_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'open-telemetry-data.csv')
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return None, "Error: 'open-telemetry-data.csv' not found in the same directory as the script."
    
    # Parsing the JSON in the TRACE column
    spans_data = []
    for _, row in df.iterrows():
        trace = json.loads(row['TRACE'])
        for span in trace['spans']:
            span['trace_id'] = row['ID']
            span['created'] = row['CREATED']
            spans_data.append(span)
    
    spans_df = pd.DataFrame(spans_data)
    
    # Cleaning and processing data
    spans_df['created'] = pd.to_datetime(spans_df['created'], format='%d-%b-%Y %H:%M:%S', errors='coerce')
    spans_df['duration'] = pd.to_numeric(spans_df['duration'], errors='coerce')
    spans_df['http.response.decoded_size'] = pd.to_numeric(spans_df['http.response.decoded_size'], errors='coerce')
    spans_df['http.first_byte_time'] = pd.to_numeric(spans_df['http.first_byte_time'], errors='coerce')
    
    # Extracting file type from http.url
    def get_file_type(url):
        if isinstance(url, str):
            match = re.search(r'\.(\w+)(?:\?.*)?$', url)
            return match.group(1).lower() if match else 'other'
        return 'other'
    
    spans_df['file_type'] = spans_df['http.url'].apply(get_file_type)
    
    return spans_df, None

# Loading data
spans_df, error_message = load_and_parse_data()

# Defining layout
if error_message:
    app.layout = html.Div(
        className="container mx-auto p-4",
        children=[
            html.H1("OpenTelemetry Dashboard", className="text-3xl font-bold mb-4 text-center"),
            html.P(error_message, className="text-red-500 text-center")
        ]
    )
else:
    # Preparing data for visualizations
    # Bar chart: Average duration by file type
    avg_duration_by_type = spans_df[spans_df['event'] == 'resource'].groupby('file_type')['duration'].mean().reset_index()
    bar_fig = px.bar(
        avg_duration_by_type,
        x='file_type',
        y='duration',
        title='Average Resource Load Time by File Type',
        labels={'duration': 'Average Duration (ms)', 'file_type': 'File Type'},
        color='duration',
        color_continuous_scale='Viridis'
    )
    bar_fig.update_layout(font=dict(size=12), title_x=0.5)

    # Pie chart: Distribution of event types
    event_counts = spans_df['event'].value_counts().reset_index()
    event_counts.columns = ['event', 'count']
    pie_fig = px.pie(
        event_counts,
        names='event',
        values='count',
        title='Distribution of Event Types',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    pie_fig.update_layout(font=dict(size=12), title_x=0.5)

    # Scatter plot: Resource size vs. load time
    scatter_data = spans_df[spans_df['event'] == 'resource'][['http.response.decoded_size', 'duration', 'http.url', 'file_type']].dropna()
    scatter_fig = px.scatter(
        scatter_data,
        x='http.response.decoded_size',
        y='duration',
        color='file_type',
        hover_data=['http.url'],
        title='Resource Size vs. Load Time',
        labels={'http.response.decoded_size': 'Resource Size (Bytes)', 'duration': 'Load Time (ms)'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    scatter_fig.update_layout(font=dict(size=12), title_x=0.5)

    # Table: Summary by container.id
    table_data = spans_df.groupby('container.id').agg({
        'duration': ['mean', 'count'],
        'http.response.decoded_size': 'sum'
    }).reset_index()
    table_data.columns = ['Page', 'Avg Duration (ms)', 'Request Count', 'Total Size (Bytes)']
    table_data['Avg Duration (ms)'] = table_data['Avg Duration (ms)'].round(2)
    table_data['Total Size (Bytes)'] = table_data['Total Size (Bytes)'].apply(lambda x: f"{int(x):,}")

    # Finding an interesting fact
    largest_resource = spans_df[spans_df['event'] == 'resource'].loc[spans_df['http.response.decoded_size'].idxmax()]
    interesting_fact = (
        f"The largest resource loaded was '{largest_resource['http.url'].split('/')[-1]}' "
        f"with a size of {int(largest_resource['http.response.decoded_size']):,} bytes, "
        f"taking {largest_resource['duration']:.2f} ms to load."
    )

    # Defining dashboard layout
    app.layout = html.Div(
        className="container mx-auto p-4",
        children=[
            html.H1("OpenTelemetry Dashboard", className="text-3xl font-bold mb-4 text-center text-blue-700"),
            html.P(
                f"Data analyzed from {spans_df['created'].min().strftime('%Y-%m-%d %H:%M:%S')} to "
                f"{spans_df['created'].max().strftime('%Y-%m-%d %H:%M:%S')}",
                className="text-center text-gray-600 mb-6"
            ),
            # Interesting Fact
            html.Div(
                className="bg-blue-100 p-4 rounded-lg mb-6",
                children=[
                    html.H2("Interesting Fact", className="text-xl font-semibold mb-2"),
                    html.P(interesting_fact, className="text-gray-700")
                ]
            ),
            # Bar Chart
            html.Div(
                className="mb-6",
                children=[
                    dcc.Graph(figure=bar_fig, className="bg-white p-4 rounded-lg shadow")
                ]
            ),
            # Pie Chart
            html.Div(
                className="mb-6",
                children=[
                    dcc.Graph(figure=pie_fig, className="bg-white p-4 rounded-lg shadow")
                ]
            ),
            # Scatter Plot
            html.Div(
                className="mb-6",
                children=[
                    dcc.Graph(figure=scatter_fig, className="bg-white p-4 rounded-lg shadow")
                ]
            ),
            # Table
            html.Div(
                className="mb-6",
                children=[
                    html.H2("Page Summary", className="text-xl font-semibold mb-2"),
                    dash_table.DataTable(
                        columns=[
                            {"name": col, "id": col} for col in table_data.columns
                        ],
                        data=table_data.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '5px',
                            'fontSize': '12px'
                        },
                        style_header={
                            'backgroundColor': '#3b82f6',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f9fafb'
                            }
                        ]
                    )
                ]
            )
        ]
    )

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
