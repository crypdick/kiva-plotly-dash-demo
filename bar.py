#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:14:35 2018

@author: beaubritain
"""
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

kiva = pd.read_csv(
    'kiva_loans.csv')


len(kiva.activity.unique()) #shows there are 163 unique activities


top5 = kiva.groupby('activity').size().sort_values(ascending=False)[0:5] #lets look at top 10

df = kiva[kiva['country'].isin(top5.index)]

app = dash.Dash(__name__)


app.layout = html.Div([
   html.H1(
        children='Top 5 activities for loans',
        style={
            'textAlign': 'center',
            'color': '#7F7F7F'
        }
    ),    
    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': top5.index,
                    'y': top5,
                    'type': 'bar',
                    'opacity': .6
                }
            
            ],
            'layout': go.Layout(
                xaxis={ 'title': 'Activity'},
                yaxis={'title': 'Count'},
            )
        }
            
        
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)