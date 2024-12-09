# imports
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback,  dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

dirpath = os.getcwd()
input_dir = os.path.join(dirpath, "data")


file_dict = [{'label': "_".join(file.split("_")[:5]), "value": file} for file in os.listdir(input_dir)]
rad_dict = [{'label': '0.025', 'value': 0.025},{'label': 0.045, 'value': 0.045},{'label': '0.08', 'value': 0.08}]
knot_dict = [{'label': '7', 'value': 7},{'label': '11', 'value': 11},{'label': '15', 'value': 15},{'label': '21', 'value': 21}]
q_dict = [{'label': '1', 'value': 1},{'label': '2', 'value': 2},{'label': '3', 'value': 3},{'label': '4', 'value': 4}]


def filter_df(filepath, q, rad, knots):
    df = pd.read_csv(filepath, names=['x', 'y', 'z', 'sec' , 'rad', 'knots', 'q'], header=None)
    df2 = df.loc[((df.q == q) & (df.knots == knots) & (df.rad == rad)), :]
    return df2

def make_plot(points_filtered):
    points = points_filtered.loc[points_filtered.sec == 'r']
    fig = go.Figure(data=[go.Scatter3d(x = points.x, y = points.y, z=points.z,mode='markers', marker=dict(size=2, color="gray", opacity=0.8), name = "raw")])
    points = points_filtered.loc[points_filtered.sec == 't']
    fig.add_trace(go.Scatter3d(x = points.x, y = points.y, z=points.z, mode='markers', marker=dict(color="red", size = 2), name = "teat", visible='legendonly'))
    points = points_filtered.loc[points_filtered.sec == 'u']
    fig.add_trace(go.Scatter3d(x = points.x, y = points.y, z=points.z, mode='markers', marker=dict(color="blue", size = 2), name = "udder"))

    fig.update_layout(paper_bgcolor="black", font_color = "white", plot_bgcolor = "black",  width=1500, height=1000)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig


def blank_fig():
    fig = go.Figure(go.Scatter3d(x=[], y = [], z=[]))
    fig.update_layout(paper_bgcolor="black")
    fig.update_layout(legend_font_color="white", width=1500, height=1000)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

MENU_STYLE = {
    'backgroundColor': 'black',
    'color': 'white',
}

sidebar = html.Div(
    [
        html.H2("Udder", className="display-4"),
        html.Hr(),
        html.P(
            "choose a cow radius, number of knots, and quarter", className="lead"
        ),
        html.Label("Rad:"),
        dcc.RadioItems(id = 'rad_btn', options=rad_dict, value= 0.045),

        html.Label("konts:"),
        dcc.RadioItems(id = 'kn-btn', options=knot_dict, value=11),

        html.Label("Q:"),
        dcc.RadioItems(id = 'q-btn', options=q_dict, value=1),
        
        html.Label("Cow ID:"),
        dcc.Dropdown(id='cows-dpdn',options= file_dict, value = '1023_20231117_124217_frame_100_udder__out.csv', style = MENU_STYLE),

    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(
[html.Div(
             [dbc.Row(
                [dbc.Col([dcc.Graph(id='graph', figure = blank_fig())])])])
], id="page-content", style=CONTENT_STYLE)


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


if __name__ == '__main__':
    app.run()