#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 19:18:43 2018

@author: beaubritain, Richard Decal
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Import your dataframe from a csv with pandas
df = pd.read_csv('data/kiva_loans.csv')

##### Beau graphs
# subset for important columns
df = df[['term_in_months', 'loan_amount', 'lender_count', 'funded_amount',
         'borrower_genders', 'repayment_interval', 'country', 'date']]
# subset for top 2 (number of loans) country values and USA to compare to
country_values = ['Philippines', 'Kenya', 'United States']
Beau_df = df[df['country'].isin(country_values)]
# sample to improve speed
a = Beau_df.sample(5000)

# len(kiva.activity.unique()) #shows there are 163 unique activities

top5 = df.groupby('activity').size().sort_values(ascending=False)[
       0:5]  # lets look at top 5
######## /Beau graphs



###### Richard maps
# converting dates from string to DateTime objects gives nice tools
df['date'] = pd.to_datetime(df['date'])
# for example, we can turn the full date into just a year
df['year'] = df.date.dt.to_period("Y")
# then convert it to integers so you can do list comprehensions later
# astype(int) expects a strings, so we need to go Period -> str -> int
# we want ints so we can find the min, max, etc later
df['year'] = df.year.astype(str).astype(int)



######

app = dash.Dash()

app.layout = html.Div(className='container', children=[
    html.H1(children='Top 3 countries Violin distributions',  # add a title
            style={
                'textAlign': 'center',  # center the header
                'color': '#7F7F7F'
            # https://www.biotechnologyforums.com/thread-7742.html more color code options
            }),
    html.Hr(),
    html.Div(className='two columns', children=[
        dcc.RadioItems(  # buttons that select which y value in violin plots
            id='items',
            options=[
                {'label': 'term in months', 'value': 'term_in_months'},
                {'label': 'loan amount', 'value': 'loan_amount'},
                {'label': 'lender count', 'value': 'lender_count'},
                {'label': 'funded amount', 'value': 'funded_amount'}
            ],
            value='term_in_months',
            style={'display': 'block',
                   'textAlign': 'center',
                   'color': '#7FDBFF'}
        ),
        html.Hr(),
        dcc.RadioItems(  # more options
            id='points',
            options=[
                {'label': 'Display All Points', 'value': 'all'},
                {'label': 'Hide Points', 'value': False},
                {'label': 'Display Outliers', 'value': 'outliers'},
                {'label': 'Display Suspected Outliers',
                 'value': 'suspectedoutliers'},
            ],
            value='all',
            style={'display': 'block',
                   'textAlign': 'center',
                   'color': '#7FDBFF'}
        ),
    ]),
    html.Div(dcc.Graph(id='graph'), className='ten columns'),
    html.H1(
        children='Top 5 activities for loans',
        style={
            'textAlign': 'center',  # center the header
            'color': '#7F7F7F'
        # https://www.biotechnologyforums.com/thread-7742.html more color code options
        }
    ),
    html.Div(dcc.Graph(  # add a bar graph to dashboard
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': top5.index,
                    'y': top5,
                    'type': 'bar',
                    'opacity': .6  # changes the bar chart's opacity
                }

            ],
            'layout': go.Layout(
                xaxis={'title': 'Activity'},
                yaxis={'title': 'Count'},
            )
        }

    ))
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
                'x': a['country'][a['country'] == 'Philippines'],
            # specify a violin plot filtered 'value' of data column
                'y': a[value],
                'text': ['Sample {}'.format(i) for i in range(len(Beau_df))],
                'points': points,
                'jitter': .7  # set the space of points
            },
            {
                'type': 'violin',
                'x': a['country'][a['country'] == 'Kenya'],
                'y': a[value],
                'text': ['Sample {}'.format(i) for i in range(len(Beau_df))],
                'points': points,
                'jitter': .7
            },
            {
                'type': 'violin',
                'x': a['country'][a['country'] == 'United States'],
                'y': a[value],
                'text': ['Sample {}'.format(i) for i in range(len(Beau_df))],
                'points': points,
                'jitter': .7
            }
        ],

        'layout': go.Layout(
            yaxis={'title': value},
            showlegend=False
            # since we listed them as different dictionaries within 'data' they are automatically separated by color with a legend. Remove this
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
