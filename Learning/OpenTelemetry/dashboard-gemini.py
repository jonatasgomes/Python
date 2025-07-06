import pandas as pd
import json
import os
import dash
from dash import dcc, html, dash_table
import plotly.express as px
from dash.dependencies import Input, Output

# --- 1. File Loading (Corrected) ---
# Construct a reliable path to the CSV file, assuming it's in the same directory as the script.
try:
    file_path = os.path.join(os.path.dirname(__file__), 'open-telemetry-data.csv')
    df = pd.read_csv(file_path)
except FileNotFoundError:
    # Fallback for environments where __file__ is not defined (like some notebooks)
    df = pd.read_csv('open-telemetry-data.csv')


# --- 2. Data Processing (Corrected Time Formatting) ---
# Parse the 'TRACE' column, which contains JSON data.
all_spans = []
for index, row in df.iterrows():
    try:
        # Ensure the trace is a string before loading
        trace_str = row['TRACE']
        if not isinstance(trace_str, str):
            continue
        
        trace_data = json.loads(trace_str)
        spans = trace_data.get('spans', [])
        
        # Add the 'ID' and 'CREATED' from the original CSV to each span
        for span in spans:
            span['ID'] = row['ID']
            span['CREATED'] = row['CREATED']
            all_spans.append(span)
            
    except (json.JSONDecodeError, TypeError):
        # Handle cases where 'TRACE' is not a valid JSON string or not a string at all.
        # print(f"Skipping row {index} due to invalid trace data.") # Optional: for debugging
        continue

# Create a new DataFrame from the list of all spans.
spans_df = pd.DataFrame(all_spans)

# Convert Unix-style timestamp columns to datetime objects.
# We specify the unit as 'ms' (milliseconds) for numeric timestamps.
# For the 'CREATED' column, we first ensure it's numeric, then convert.
for col in ['start_time', 'end_time', 'ts', 'CREATED']:
    if col in spans_df.columns:
        # Coerce non-numeric values to NaT (Not a Time), preventing errors.
        numeric_col = pd.to_numeric(spans_df[col], errors='coerce')
        # Explicitly convert from Unix timestamp in milliseconds to datetime.
        # This resolves the UserWarning.
        spans_df[col] = pd.to_datetime(numeric_col, unit='ms', errors='coerce')

# Drop rows where key datetime conversions might have failed
spans_df.dropna(subset=['start_time', 'end_time', 'duration'], inplace=True)


# Prepare data for the component bar chart.
component_counts = spans_df['component'].value_counts().reset_index()
component_counts.columns = ['component', 'count']


# --- 3. Dashboard Creation (Corrected Imports & Layout) ---
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#f2f2f2', 'font-family': 'Arial, sans-serif'}, children=[
    html.H1(
        children='OpenTelemetry Dashboard',
        style={'textAlign': 'center', 'color': '#333333', 'padding': '20px'}
    ),
    html.Div(
        children='A dashboard to visualize OpenTelemetry span data.',
        style={'textAlign': 'center', 'color': '#666666', 'padding-bottom': '20px'}
    ),

    # Container for the graphs
    html.Div(style={'padding': '20px'}, children=[
        # Graph 1: Histogram of Span Durations
        html.Div(style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'vertical-align': 'top'}, children=[
            dcc.Graph(
                id='duration-histogram',
                figure=px.histogram(
                    spans_df,
                    x="duration",
                    title="Distribution of Span Durations (ms)",
                    labels={'duration': 'Duration (ms)'}
                ).update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font_color='#333333')
            )
        ]),

        # Graph 2: Bar Chart of Spans per Component
        html.Div(style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'vertical-align': 'top'}, children=[
            dcc.Graph(
                id='component-bar-chart',
                figure=px.bar(
                    component_counts,
                    x='component',
                    y='count',
                    title="Number of Spans per Component",
                    labels={'component': 'Component', 'count': 'Count'}
                ).update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font_color='#333333')
            )
        ]),
    ]),

    # Data Table
    html.Div(style={'padding': '20px'}, children=[
        html.H3("Span Data", style={'color': '#333333'}),
        dash_table.DataTable(
            id='data-table',
            # A curated list of the most relevant columns
            columns=[{"name": i, "id": i} for i in ['span_id', 'trace_id', 'duration', 'component', 'event', 'http.url']],
            data=spans_df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
                'whiteSpace': 'normal',
                'textAlign': 'left'
            },
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
    ])
])

# --- 4. Run Application (Corrected) ---
if __name__ == '__main__':
    # Use app.run() instead of the obsolete app.run_server()
    app.run(debug=True)
