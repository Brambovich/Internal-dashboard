import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import datetime as datetime
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
import dash_gif_component as gif

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20vw",
    "padding": "1vw 1vw",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "position": "fixed",
    "margin-left": "20vw",
    "margin-right": "2vw",
    "width": "80vw",
    "padding": "1vw 1vw",
    "height": "100vw",
}

sidebar = html.Div(
    [
#         gif.GifPlayer(
#             gif='assets/animation1Unda.gif',
#             still='assets/still1Unda.png',
#             autoplay=True,
#         ),
        html.H1("Undagrid", style={'textAlign': 'center'}),
        html.H2("Nestor Dashboard", className="display-7", style={'textAlign': 'center'}),
        html.Hr(),
        html.P(
            "Node selection:", className="lead", style={'textAlign': 'center'}
        ),
        dbc.Input(id='nodeId', value='081001CVC4', type='text', style={
            'width': '100%',
            'textAlign': 'center',
            'margin-bottom': '10px'
        }),
        dbc.Container([
            dbc.Row([
                dbc.Col(        
                    dbc.Button('Add', id='add-node', style={
                        'width': '80%',
                        'textAlign': 'center',
                        'margin-bottom': '10px'
                    })
                ),
                dbc.Col(        
                    dbc.Button('Clear', id='clear-node', style={
                        'width': '80%',
                        'textAlign': 'center',
                        'margin-bottom': '10px'
                    })
                )
            ])
        ]),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '100%',
                'lineHeight': '200%',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'color': 'grey',
                'margin-bottom': '20px'
            },
        # Allow multiple files to be uploaded
        multiple=False
        ),
        html.P(
            "Date selection:", className="lead", style={'textAlign': 'center'}
        ),
        html.Div([dcc.DatePickerRange(
            id='my-date-picker-range',
            display_format='DD-MM-YYYY',
            minimum_nights=1,
            initial_visible_month=datetime.now(),
            start_date=(datetime.now()-timedelta(days=10)),
            end_date=datetime.now()
            )], 
            style={
                'width': '100%',
                'display':'flex',
                'align-items': 'center',
                'justify-content':'center',
                'padding-bottom': '10px'
            }
        ),
        # html.P(
        #     "Add a group:", className="lead", style={'textAlign': 'center'}
        # ),
        # dbc.Input(id='group-input', type='text', style={
        #     'width': '100%',
        #     'textAlign': 'center',
        #     'margin-bottom': '10px'
        # }),
        # dbc.Button('Add group', id='add-group', style={
        #             'width': '100%',
        #             'textAlign': 'center',
        #             'margin-bottom': '10px',
        # }),
        html.Hr(style={
            'margin-bottom':'30px'
        }),
        dash_table.DataTable(id='node-table', 
            style_table={
                'height': '200px',
                'overflowX': 'auto'
            },
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            row_selectable='multi',
            page_size=5,
        )    
    ],
    style=SIDEBAR_STYLE,
)



content = html.Div(
            dbc.Tabs([
                dbc.Tab(id='voltage_tab', children=[
                    html.Div([
                        dcc.Graph(id='voltage_figure')],
                        style = {
                        'width': '100%',
                        'height': '100%'
                        }
                        )
                ]),
                dbc.Tab(id='location_tab', children=[
                    dcc.Graph(id='location_figure')
                ]),
                dbc.Tab(id='delay_tab', children=[
                    dcc.Graph(id='delay_figure')
                ]),
                dbc.Tab(id='timeline_tab', children=[
                    html.Br(),
                    dcc.Dropdown(
                        id='timeline-dropdown'
                    ),
                    html.Br(),
                    dcc.Graph(id='timeline_figure')
                ]),
                dbc.Tab(id='table_tab', children=[
                    html.Br(),
                    dcc.Dropdown(
                        id='table_dropdown',
                        options=[
                            {'label': 'log.log', 'value': 'log'},
                            {'label': 'log.voltage', 'value': 'voltage'},
                            {'label': 'log.scan', 'value': 'scan'},
                            {'label': 'log.start', 'value': 'start'},
                            {'label': 'log.nbiot', 'value': 'nbiot'},
                            {'label': 'log.cellInformation', 'value': 'cellInformation'},
                            {'label': 'log.pressureRecord', 'value': 'pressureRecord'}
                        ],
                        value='log'
                    ),
                    html.Br(),
                    dash_table.DataTable(
                        id ='table',
    #                     columns=[{'name': 'nodeId', 'id': 'nodeId'}],
                        style_table={
                            'overflowX': 'auto'
                        },
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'fontSize' : 15,
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        style_cell={
                            'textAlign': 'left',
                        },
                        page_size=15,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                    )
                ])
        ], id='tabs'), style=CONTENT_STYLE)

def make_layout():
    return html.Div([
        dcc.Store(id='node_list_memory'),
        dcc.Store(id='node_list_selected'),
        dcc.Location(id="url"), 
        sidebar, 
        content
    ])
    