import dash_bootstrap_components as dbc
import auth0
import os

import dash_auth
from dash import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

