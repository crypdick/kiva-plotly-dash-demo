#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:36:03 2018

@author: beaubritain
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

kiva = pd.read_csv(
    'kiva_loans.csv')
#subset for important columns 
df = kiva[['term_in_months','loan_amount', 'lender_count', 'funded_amount', 'borrower_genders', 'repayment_interval', 'country']]
#subset for top 2 (number of loans) country values and USA to compare to 
country_values = ['Philippines', 'Kenya', 'United States']
df = df[df['country'].isin(country_values)]
#sample to improve speed
a = df.sample(5000)

app = dash.Dash()

app.layout = html.Div(className='container', children=[
    html.H1('Top 3 countries Violin distributions'),
    html.Hr(),
    html.Div(className='two columns', children=[
        dcc.RadioItems(
            id='items',
            options=[
                {'label': 'term in months', 'value': 'term_in_months'},
                {'label': 'loan amount', 'value': 'loan_amount'},
                {'label': 'lender count', 'value': 'lender_count'},
                {'label': 'funded amount', 'value': 'funded_amount'}
            ],
            value= 'term_in_months',
            style={'display': 'block'}
        ),
        html.Hr(),
        dcc.RadioItems(
            id='points',
            options=[
                {'label': 'Display All Points', 'value': 'all'},
                {'label': 'Hide Points', 'value': False},
                {'label': 'Display Outliers', 'value': 'outliers'},
                {'label': 'Display Suspected Outliers', 'value': 'suspectedoutliers'},
            ],
            value='all',
            style={'display': 'block'}
        ),
    ]),
    html.Div(dcc.Graph(id='graph'), className='ten columns')
])
        
@app.callback(
    Output('graph', 'figure'), [
    Input('items', 'value'),
    Input('points', 'value')])
def update_graph(value, points):
    return {
        'data': [
            {
                'type': 'violin',
                'x': a['country'][a['country']== 'Philippines'],
                'y': a[value],
                'text': ['Sample {}'.format(i) for i in range(len(df))],
                'points': points,
                'jitter': .7
            },
            {
                'type': 'violin',
                'x': a['country'][a['country']== 'Kenya'],
                'y': a[value],
                'text': ['Sample {}'.format(i) for i in range(len(df))],
                'points': points,
                'jitter': .7
            },
            {
                'type': 'violin',
                'x': a['country'][a['country']== 'United States'],
                'y': a[value],
                'text': ['Sample {}'.format(i) for i in range(len(df))],
                'points': points,
                'jitter': .7
            }  
        ],
        
        'layout': {
            'showlegend': False
        }
    }
if __name__ == '__main__':
    app.run_server(debug=True)