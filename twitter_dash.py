#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 11:43:16 2018

@author: mohitbeniwal
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from twitter_Live import main as df
import plotly.graph_objs as go


df1=pd.DataFrame()
app_colors = {
    'background': '#FFFFFF',
    'text': '#000000'}
def color(i):
    if(i=='positive'):
        return 'green'
    elif(i=='negative'):
        return 'red'
    else:
        return 'gray'

def generate_table(df, max_rows=10):
    return html.Table(className="responsive-table",
                      children=[
                          html.Thead(
                              html.Tr(
                                  children=[
                                      html.Th(col.title()) for col in df.columns.values],
                                  style={'color':app_colors['text']}
                                  )
                              ),
                          html.Tbody(
                              [
                                  
                              html.Tr(
                                  children=[
                                      html.Td(data) for data in d
                                      ], style={'color':app_colors['text'],
                                                'background-color':color(d[1])}
                                  )
                               for d in df.values.tolist()])
                          ]
    )

def generate_graph(df):
    return html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['sentiment'] == i]['time'],
                    y=df[df['sentiment'] == i]['retweet_count'],
                    text=df[df['sentiment'] == i]['clean_text'],
                    mode='markers',
                    #opacity=0.7,
                    marker={
                        'size': 15,
                        'color': color(i) ,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.sentiment.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time','showgrid':True,},
                yaxis={'title': 'NO. of Retweet'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
            ])
def generate_pie(pos,neg,neu,sentiment_term):
    labels = ['Positive','Negative','Neutral']
    values = [pos,neg,neu]
    colors = ['#007F25', '#800000','grey']

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='value', 
                   textfont=dict(size=20, color=app_colors['text']),
                   marker=dict(colors=colors, 
                               line=dict(color=app_colors['background'], width=2)))

    return html.Div([
    dcc.Graph(
        id='pie',
        figure={"data":[trace],'layout' : go.Layout(
                                                  title='Positive, Negative and neutral sentiment for "{}"'.format(sentiment_term),
                                                  font={'color':app_colors['text']},
                                                  plot_bgcolor = app_colors['background'],
                                                  paper_bgcolor = app_colors['background'],
                                                  showlegend=True)} )
            ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H2(children='Twitter Sentiment Alalysis Tool',style={'textAlign':'center'}),
    html.Div([
    dcc.Input(id='input-1-state',
    placeholder='Enter a Keyword...',
    type='text',
    value=''),
    dcc.Input(id='input-2-state',
    placeholder='No. of tweets...',
    type='text',
    value=''),
    html.Button(id='submit-button', n_clicks=0, children='Submit')],style={'textAlign':'center'}),
    html.Div(id='output-state')
])
@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
        
def update_output(n_clicks,input1="",input2=1):
    df1=df(input1,input2)
    positiveTweets=df1[1]
    negativeTweets=df1[2]
    neturalTweets=df1[3]
    positive_retweet_count=0
    negative_retweet_count=0
    neutral_retweet_count=0
    positive_retweet_count=positiveTweets['retweet_count'].sum()+len(positiveTweets)
    negative_retweet_count=negativeTweets['retweet_count'].sum()+len(negativeTweets)
    neutral_retweet_count=neturalTweets['retweet_count'].sum()+len(neturalTweets)



    return  generate_graph(df1[0]),generate_pie(positive_retweet_count,negative_retweet_count,neutral_retweet_count,input1),generate_table(df1[0])


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    


    
