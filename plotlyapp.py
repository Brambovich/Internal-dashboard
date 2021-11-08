import os
import sys
from dotenv import load_dotenv
load_dotenv()

from functions.database_functions import retrieve_df, parse_contents
from functions.layout_functions import generate_table, testfunc
from layout import make_layout
from callbacks import figure_callbacks, node_list_callbacks
from mainapp import app

app.layout = make_layout
if __name__ == '__main__':
    app.run_server(debug=True)