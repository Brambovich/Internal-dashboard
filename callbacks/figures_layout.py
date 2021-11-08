import plotly.graph_objects as go
import plotly.express as px

figure_layouts = {}

font_dict=dict(family='Arial',
               size=22,
               color='black'
               )
general_fig = px.line()
general_fig.update_layout(
            font=font_dict,  # font formatting
            plot_bgcolor='white',  # background color
            margin=dict(r=20,t=20,b=10)  # remove white space 
            )
general_fig.update_yaxes(
            showline=True,  # add line at x=0
            linecolor='black',  # line color
            linewidth=2.4, # line size
            ticks='outside',  # ticks outside axis
            tickfont=font_dict, # tick label font
            mirror='allticks',  # add ticks to top/right axes
            tickwidth=2.4,  # tick width
            tickcolor='black',  # tick color
            showgrid=True,
            gridcolor='lightgrey',
            
                zeroline=True,
            zerolinecolor = 'grey',
    zerolinewidth=2
            )
general_fig.update_xaxes(
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
            tickcolor='black'
            )
general_layout = general_fig.layout


voltage_fig = px.line()
voltage_fig.layout = general_layout
voltage_fig.update_yaxes(title_text='Voltage',  # axis label
                 range=(0, 4500)
            )
voltage_fig.update_xaxes(title_text='Time'
            )
figure_layouts['voltage'] = voltage_fig.layout

delay_fig = px.line()
delay_fig.layout = general_layout
delay_fig = general_fig
delay_fig.update_yaxes(title_text='Delay'  # axis label
            )
delay_fig.update_xaxes(title_text='Time'
            )
figure_layouts['delay'] = delay_fig.layout
