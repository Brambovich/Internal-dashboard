import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from mainapp import app
from dash.dependencies import Input, Output, State
from functions.database_functions import retrieve_df, parse_contents, correctTs
from functions.layout_functions import generate_table, testfunc

from callbacks.figures_layout import figure_layouts

@app.callback(Output("voltage_figure", "figure"),
              Output("voltage_tab", "disabled"),
              Output("voltage_tab", "label"),
              Input('node_list_selected', 'data'),
              Input("my-date-picker-range", "start_date"),
              Input("my-date-picker-range", "end_date")
)

def update_voltage_figure(node_list, start_date, end_date):
    if (type(node_list) == list):
        if len(node_list) == 0:
            fig = go.Figure(data=go.Scatter(x=[], y=[]))
            fig.layout = voltage_layout
            return dash.no_update, True, "No nodes selected"
        df = retrieve_df(node_list, start_date, end_date, 'log.voltage', ['nodeId', 'gatewayTs', 'maxVoltage'])
        if df.empty:
            return dash.no_update, True, "No data in selected time"

        fig = px.line(df, x="gatewayTs", y="maxVoltage", color="nodeId")
        fig.layout = figure_layouts['voltage']
        return fig, False, "Voltage"
    else:
        fig = go.Figure(data=go.Scatter(x=[], y=[]))

        return dash.no_update, True, "No nodes selected"
    
    
@app.callback(Output("delay_figure", "figure"),
              Output("delay_tab", "disabled"),
              Output("delay_tab", "label"),
              Input('node_list_selected', 'data'),
              Input("my-date-picker-range", "start_date"),
              Input("my-date-picker-range", "end_date")
)
def update_delay_figure(node_list, start_date, end_date):
    if (type(node_list) == list):
        if len(node_list) == 0:
            return dash.no_update, True, "No nodes selected"
        df = retrieve_df(node_list, start_date, end_date, 'log.log', ['nodeId', 'value', 'ts', 'gatewayTs'])
        if df.empty:
            return dash.no_update, True, "No data in selected time"
        #        df = pd.concat([df, df['value'].apply(pd.Series)], axis = 1).drop('value', axis = 1)

        df['correction'] = df['value'].apply(func=correctTs)
        df['tsCorrected'] = df['ts'] + df['correction']

        df['delay'] = (df['gatewayTs'].astype('int') - df['tsCorrected'].astype('int')) / 1000000000
        df = df[df['delay'] < 1 * 24 * 3600]
        fig = px.line(df, x="gatewayTs", y="delay", color="nodeId")
        fig.layout = figure_layouts['delay']
        return fig, False, "Delay"
    else:
        return dash.no_update, True, "No nodes selected"
        

@app.callback(Output("location_figure", "figure"),
              Output("location_tab", "disabled"),
              Output("location_tab", "label"),
              Input('node_list_selected', 'data'),
              Input("my-date-picker-range", "start_date"),
              Input("my-date-picker-range", "end_date")
)
def update_location_figure(node_list, start_date, end_date):
    if (type(node_list) == list):
        if len(node_list) == 0:
            return dash.no_update, True, "No nodes selected"
        df = retrieve_df(node_list, start_date, end_date, 'log.location', ['nodeId', 'lat', 'lon', 'ts', 'gatewayTs', 'accuracy', 'isFix'])
        df = df[df['isFix'] == True]
        if df.empty:
            return dash.no_update, True, "Location(not enough data...)"
        else:
            MAPBOX_token = "pk.eyJ1IjoidW5kYWdyaWQiLCJhIjoiY2loZXZycHdkMGxpOXQ0bHo0cGw2anMwaSJ9.b7Dj_o8jv9lVEyyrnUd9Yw"
            px.set_mapbox_access_token(MAPBOX_token)
            fig = px.line_mapbox(df, lat="lat", lon="lon", hover_name="ts", color="nodeId",
                                 hover_data=["ts", "gatewayTs", "accuracy"], zoom=12)


            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            return fig, False, "Location"
    else:
        return dash.no_update, True, "No nodes selected"
            
        
        

@app.callback(Output("table", "data"),
              Output("table", "columns"),
              Output("table_tab", "disabled"),
              Output("table_tab", "label"),
              Input("table_dropdown", "value"),
              Input('node_list_selected', 'data'),
              Input("my-date-picker-range", "start_date"),
              Input("my-date-picker-range", "end_date")
)
def update_table(view, node_list, start_date, end_date):
    if (type(node_list) == list):
        if len(node_list) == 0:
            return [], dash.no_update, True, "No nodes selected"
        df = retrieve_df(node_list, start_date, end_date, 'log.'+view, [])
        if df.empty:
            return [], dash.no_update, True, "No data in selected time"
        #print("inside updatetable 1, columns:\n", df.columns)
        #df = df.select_dtypes(exclude = object)
        try:
            df.drop(columns=['value'], inplace=True)
        except:
            pass
        #print("inside updatetable 2, columns:\n", df.columns)
        columns_list = [{'name': str(i), 'id': (i)} for i in df.columns]

        return df.to_dict('records'), columns_list, False, "Table View"
    else:
        return [], dash.no_update, True, "No nodes selected"


@app.callback(Output("timeline_figure", "figure"),
              Output("timeline_tab", "disabled"),
              Output("timeline_tab", "label"),
              Input("timeline-dropdown", "value"),
              Input('node_list_selected', 'data'),
              Input("my-date-picker-range", "start_date"),
              Input("my-date-picker-range", "end_date")
)
def update_timeline(node_id, node_list, start_date, end_date):
    if len(node_list) < 1:
        return dash.no_update, True, "No nodes selected"
    if node_id == None:
        node_id = node_list[0]
    df_state = retrieve_df([node_id], start_date, end_date, 'log.state', ['nodeId', 'stateName', 'value', 'ts', 'gatewayTs'])
    if df_state.empty:
        return dash.no_update, True, "No data in selected time"
    df_location = retrieve_df([node_id], start_date, end_date, 'log.location', ['nodeId', 'sessionTime', 'ts', 'isFix', 'gatewayTs'])
    df_scan = retrieve_df([node_id], start_date, end_date, 'log.scan', ['ts', 'nodeId', 'gatewayTs'])
    value = False
    start_time = datetime.now()
    list_of_dicts_log = []


    for i in df_state.stateName.unique():
        value = False
        for index, row in (df_state[df_state['stateName'] == i]).iterrows():
            #print(row['ts'], row['value'], row['changed'])
            if row['value'] == True:
                if value == False:
                    value = True
                    start_time = row['ts']
            else:
                if value == True:
                    value = False
                    end_time = row['ts']
                    dicttoappend = dict(Task=i, Start = start_time, Finish = end_time, Status = i)
                    list_of_dicts_log.append(dicttoappend)
                    
    start_time = datetime.now()
    list_of_dicts_GPS = []

    for index, row in (df_location[df_location['sessionTime'] > 0]).iterrows():
        dicttoappend = dict(Task='GPS', Finish = (row['ts'] + timedelta(seconds = row['sessionTime'])), Start = row['ts'], Status = 'Fix found' if row['isFix'] else 'no Fix')
        list_of_dicts_GPS.append(dicttoappend)
        
    start_time = datetime.now()
    list_of_dicts_scan = [] 
    for index, row in (df_scan.drop_duplicates(subset=['ts', 'nodeId'])).iterrows():
        dicttoappend = dict(Task='Scan', Start=(row['ts'] + timedelta(seconds=4)), Finish=row['ts'], Status='Scan')
        list_of_dicts_scan.append(dicttoappend)

    list_of_dicts = list_of_dicts_log + list_of_dicts_GPS + list_of_dicts_scan
    plot_df = pd.DataFrame(list_of_dicts)
    fig = px.timeline(plot_df, x_start="Start", x_end="Finish", y="Task", color="Status", color_discrete_sequence=["blue", "magenta", "green", "red", "magenta"])
    font_dict=dict(family='Arial',
                   size=22,
                   color='black'
                   )
    fig.update_layout(
                font=font_dict,  # font formatting
                plot_bgcolor='white',  # background color
                margin=dict(r=20,t=20,b=10)  # remove white space 
                )
    fig.update_yaxes(
            showline=True,  # add line at x=0
            linecolor='black',  # line color
            linewidth=2.4, # line size
            ticks='outside',
                    tickwidth=2.4,
            tickcolor='black',
            showgrid=True,
            mirror='allticks',
            gridcolor='darkgrey',
            gridwidth=2
            )
    fig.update_xaxes(
            showline=True,
            showticklabels=True,
            linecolor='black',
            linewidth=2.4,
            ticks='outside',
            tickfont=font_dict,
            mirror='allticks',
            showgrid=True,
            gridcolor='lightgrey',
            tickwidth=2.4,
            tickcolor='black',
            gridwidth=1
            )
    fig.update_yaxes(autorange="reversed")
    return fig, False, "Timeline"
