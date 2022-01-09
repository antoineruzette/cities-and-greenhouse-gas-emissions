# Created: 01/05/2021
# Author: Team Somalia

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import nlp_plots as nlpp

app = dash.Dash(__name__, title='Modern Data Analytics 2021', external_stylesheets=[dbc.themes.BOOTSTRAP])

# For heroku
server = app.server

# Tabs with plots
plot_tabs = dcc.Tabs([
    dcc.Tab(label='Frequency Plot', children=[
        dcc.Graph(id='id-freq-plot')
    ]),
    dcc.Tab(label='Network Plot', children=[
        dcc.Graph(id='id-network-plot')
    ])
])

# User inputs
region_options = [{'label': 'All regions', 'value': 'All regions'},
                  {'label': 'Africa', 'value': 'Africa'},
                  {'label': 'Europe', 'value': 'Europe'},
                  {'label': 'Latin America', 'value': 'Latin America'},
                  {'label': 'North America', 'value': 'North America'},
                  {'label': 'Middle East', 'value': 'Middle East'},
                  {'label': 'East Asia', 'value': 'East Asia'},
                  {'label': 'South and West Asia', 'value': 'South and West Asia'},
                  {'label': 'Southeast Asia and Oceania', 'value': 'Southeast Asia and Oceania'}]
region_dropdown = dcc.Dropdown(
    id="id-region",
    options=region_options,
    value='All regions'
)

inputs = dbc.Row(children=[dbc.Col(children=[
    # Slider for year
    html.P("Choose year"),
    dcc.Slider(id='id-slider-year', step=None,
               min=2013, max=2020,
               marks={
                   2013: '2013',
                   2014: '2014',
                   2015: '2015',
                   2016: '2016',
                   2017: '2017',
                   2018: '2018',
                   2019: '2019',
                   2020: '2020',
               },
               value=2017)
]), dbc.Col(children=[
    # Dropdown for region
    html.P("Choose region"),
    region_dropdown,
]), dbc.Col(children=[
    # Input for number
    html.P("Type a number outside the range 0-10"),
    dbc.Input(
        id='id-kt-number', type="number",
        min=1, max=20, step=1, value=13
    ),

])
])

# dcc.Loading(
#                     id="loading-2",
#                     children=[html.Div([html.Div(id="loading-output-2")])],
#                     type="circle",
#                 )

app.layout = html.Div(children=[
    # Title and subtitles
    html.Div(children=[
        html.Div(children=[html.H1(children='Cities and Greenhouse Gas Emissions'),
                           html.H2(children='Data Source: CDP')],
                 style={'textAlign': 'center',
                        'color': 'black'}),
        html.Div(children=[html.H3(children='Authors: Team Somalia')],
                 style={'textAlign': 'center',
                        'color': 'gray'})
    ]),
    html.Hr(),
    dcc.Loading(children=plot_tabs),
    inputs
], style={'marginLeft': 50, 'marginRight': 25})


@app.callback(
    Output('id-freq-plot', 'figure'),
    Output('id-network-plot', 'figure'),
    # Output('id-region', 'options'),
    Input('id-slider-year', 'value'),
    Input('id-region', 'value'),
    Input('id-kt-number', 'value')
)
def update_plot_tabs(year, region, number):
    freq_plot_fig = nlpp.freq_plot(year, region, number)
    network_plot_fig = nlpp.network_plot(year, region, number)
    return freq_plot_fig, network_plot_fig


if __name__ == '__main__':
    app.run_server(debug=True)
