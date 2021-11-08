import dash
import pandas as pd
from datetime import datetime, timedelta

from mainapp import app
from dash.dependencies import Input, Output, State
from functions.database_functions import retrieve_df, parse_contents, stratus_nodesfromgroup
from functions.layout_functions import generate_table, testfunc

@app.callback(Output("node_list_memory", "data"),
              Output("nodeId", "value"),
             # Input("add-group", "n_clicks"),
             Input("add-node", "n_clicks"),
             Input("clear-node", "n_clicks"),
             Input('upload-data', 'contents'),
             State('upload-data', 'filename'),
             State("nodeId", "value"),
             # State("group-input", "value"),
             State("node_list_memory", "data"))
def update_nodelist(add, clear, upload_content, upload_name, node_ID, node_list):
    node_id_value = dash.no_update
    print("UPDATE NODELIST!!\n")
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("button pressed: ", button_id)

    if button_id == "add-node":
        if type(node_list) == list:
            if node_ID not in node_list:
                node_list.append(node_ID)
        else:
            node_list = [node_ID]
        node_id_value = ""
    # elif button_id == 'add-group':
    #     node_list = stratus_nodesfromgroup(group_name)
    elif button_id == "clear-node":
        node_list = []
        node_id_value = ""
    elif button_id == "upload-data":
        print("UPLOADED DATA!: ", upload_name)
        node_list = parse_contents(upload_content, upload_name)
    print("Node list: \n", node_list)
    return node_list, node_id_value

@app.callback(Output("node_list_selected", "data"),
             Input("node_list_memory", "data"),
             Input('node-table', "derived_virtual_selected_rows")
)
def update_selected_nodes(node_list, selected_list):
    print("update the selected nodes...")
    if type(node_list) == list:
        if len(selected_list) == 0:
            print("selected nodes: ", node_list)
            return node_list
        else:
            print("selected nodes: ", [node_list[i] for i in selected_list])
            return [node_list[i] for i in selected_list]
    return []
     

@app.callback(Output("timeline-dropdown", "options"),
             Input("node_list_selected", "data"))
def update_optionslist(node_list):
    if type(node_list) == list:
        options_list = [{'label': i, 'value': i} for i in node_list]
        return options_list
    else:
        return dash.no_update


@app.callback(Output("node-table", "data"),
              Output("node-table", "columns"),
              Input("node_list_memory", "data"))
def update_nodetable(node_list):
    list_of_dicts = []
    if type(node_list) == list:
        df = retrieve_df(node_list, datetime.now() - timedelta(days = 150) , datetime.now(), 'log.start', ['nodeId', 'gatewayTs', 'firmwareVersion', 'applicationId'])
        for i in node_list:
            node_df = df[df['nodeId'] == i]
            latestfirmwareversion = node_df.tail(1)['firmwareVersion'].values[0]
            ID = node_df.tail(1)['applicationId'].values[0]
            date = node_df[node_df['firmwareVersion'] == latestfirmwareversion].head(1)['gatewayTs'].values[0]
            ts = pd.to_datetime(str(date)) 
            d = ts.strftime('%Y.%m.%d')
            dicttoappend = dict(nodeId=i, Latestfirmware = latestfirmwareversion, DateUpdated = d, latestAppID = ID)
            list_of_dicts.append(dicttoappend)
        
    columns_list = [{'name': 'nodeId', 'id': 'nodeId'}, 
                    {'name': 'Latest Firmware', 'id': 'Latestfirmware'}, 
                    {'name': 'Update date', 'id': 'DateUpdated'},
                    {'name': 'AppID', 'id': 'latestAppID'}]
    return list_of_dicts, columns_list
