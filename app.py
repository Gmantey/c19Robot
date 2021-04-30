# -*- coding: utf-8 -*-
import base64
from flask import Flask
import os
import dash
import plotly
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import pymysql
import time
from collections import deque
import hardwareDB as dataBase  # CONNECTED TO AWS RSD DATABASE
import random


group_colors = {"control": "light blue", "reference": "red"}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], server=server, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True
)

prev_data = None

# Sample Test
X = deque(maxlen=20)
X.append(1)

Y = deque(maxlen=20)
Y.append(1)


# Data for Scatter plot
homedir = os.path.dirname(os.path.abspath(__file__))
data_2 = os.path.join(homedir, 'data/study.csv')

# Card components
cards = [
    dbc.Card(
        [
            html.H2("Hey", className="card-title"),
            html.P("Model Training Accuracy", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2("Hey", className="card-title"),
            html.P("Model Test Accuracy", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2("Hey", className="card-title"),
            html.P("Train / Test Split", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
]


# App Layout
app.layout = html.Div(
    children=[
        # Error Message
        html.Div(id="error-message"),
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title",
                        children="COVID 19 WEBSITE DEMO"),
                # Learn more button
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://plot.ly/dash/pricing/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
                # LOGO
                html.Div(
                    className="div-logo",
                    children=html.Img(
                        className="logo", src=app.get_asset_url("logos/Logo_v5.png"),
                    ),
                ),
                html.H2(className="h2-title-mobile",
                        children="COVID 19 WEBSITE DEMO"),
            ],
        ),
        # Body of APP
        html.Div(
            className="row app-body",
            children=[
                html.Div(
                    className="four columns card",
                    children=[
                        # Introduction & Uploading Data
                        html.Div(
                            className="pretty_container bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("Welcome to COVID 19 Robot"),
                                        html.Br(),
                                        html.H6("Introduction"),
                                        html.P(
                                            "To develop a data-driven, autonomous, solution that allows for the safe detection and sanitation of the COVID-19 virus in different environments such as hospitals, schools, grocery stores, etc."),
                                    ],
                                ),
                                # Upload Controls
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("Upload Data File"),
                                        dcc.Upload(
                                            id="upload_data",
                                            className="upload",
                                            children=html.Div(
                                                children=[
                                                    html.P(
                                                        "Drag and Drop or "),
                                                    html.A("Select Files"),
                                                ]
                                            ),
                                            accept=".csv",
                                        ),
                                    ],
                                ),
                                # Simple Controls
                                html.H6("Select Time Frame"),
                                dcc.Dropdown(id="slct_year",
                                             options=[
                                                 {"label": "Seconds",
                                                  "value": 1},
                                                 {"label": "Minutes",
                                                  "value": 2},
                                                 {"label": "Hours",
                                                  "value": 3}, ],
                                             multi=False,
                                             value=2015,
                                             style={'width': "60%"},
                                             ),
                                html.Br(),
                                html.Button(
                                    'START', id='start_btn', n_clicks=0),
                            ],
                        )
                    ],
                ),
                # CARD CONTROLS
                html.Div(
                    className="eight columns card-left",
                    children=[
                        # Average temperature
                        html.Div(
                            className="pretty_container three columns",
                            children=[
                                html.H6("Live Temperature"),
                                html.H3(id="temp_text", children=[])],
                        ),
                        html.Div(
                            className="pretty_container three columns",
                            children=[
                                html.H6("Current Distance 1 "),
                                html.H3(id="dist1_text", children=[])],
                        ),
                        html.Div(
                            className="pretty_container three columns",
                            children=[
                                html.H6("Current Distance 2"),
                                html.H3(id="dist2_text", children=[])],
                        ),
                        html.Div(
                            className="pretty_container three columns",
                            children=[
                                html.H6("Current Distance 3 "),
                                html.H3(id="dist3_text", children=[])],
                        ),
                    ],
                ),
                # Mini Indicator
                # Graph 1
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="pretty_container bg-white",
                            children=[
                                dcc.Graph(id='live-graph', animate=True),
                                dcc.Interval(
                                    id='graph-update',
                                    interval=1*1000
                                ),
                            ],
                        )
                    ],
                ),
                dcc.Store(id="error", storage_type="memory"),
            ],
        ),
    ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback([Output(component_id='live-graph', component_property='figure'),
               Output(component_id='temp_text', component_property='children'),
               Output(component_id='dist1_text',
                      component_property='children'),
               Output(component_id='dist2_text',
                      component_property='children'),
               Output(component_id='dist3_text', component_property='children')],
              [Input(component_id='graph-update', component_property='n_intervals')])
def update_graph_scatter(input_data):
    X.append(X[-1]+1)
    data = dataBase.get_last(X[-1])

    if (len(data) == 0):
        y_data = Y[-1]
        dist1 = "--"
        dist2 = "--"
        dist3 = "--"
    else:
        y_data = data[0][0]
        dist1 = data[0][1]
        dist2 = data[0][2]
        dist3 = data[0][3]
        Y.append(y_data)

    # print(X)
    # print(Y)

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    temp_text = str(y_data)
    dist1_text = str(dist1)
    dist2_text = str(dist2)
    dist3_text = str(dist3)

    temp = "{} °F".format(temp_text)
    dist1 = "{} cm".format(dist1_text)
    dist2 = "{} cm".format(dist2_text)
    dist3 = "{} cm".format(dist3_text)

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(
                                                    range=[min(Y), max(Y)]),
                                                title='LIVE Temperature Data',
                                                xaxis_title="Time",
                                                yaxis_title="Temperature °F",
                                                )}, temp, dist1, dist2, dist3


if __name__ == "__main__":
    app.run_server(debug=True)
