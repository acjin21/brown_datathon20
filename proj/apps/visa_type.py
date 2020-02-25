# import dash_core_components as dcc
# import dash_html_components as html

from app import app, links

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

file='./data/visa_data.xlsx'
xl = pd.ExcelFile(file)
df_region = xl.parse('ByRegion')
df_country = xl.parse('Top40CountriesPleasure')

col_name='World Region/Country of Residence (COR)'
world_regions = list(df_region[col_name]) # list of regions
countries = list(df_country[col_name])

# these are the same for both sheets
labels = ['Business', 'Pleasure', 'Student']
column_list = ['Total: Business', 'Total: Pleasure', 'Total: Student']

# create multiple traces for pie chart
region_data=[]
country_data=[]
for i in range(len(world_regions)):
    visible=False;
    if i == 0: visible=True;

    target_region = world_regions[i] # get string of region
    sub_df = df_region.loc[df_region[col_name] == target_region] # specific row corresponding to target_region
    values = sub_df[column_list].values[0] # get values from each column in column_list
    trace = (dict(labels=labels,
                 values=values,
                 type='pie',
                 visible=visible))
    region_data.append(trace)

for i in range(len(countries)):
    visible=False;
    if i == 0: visible=True;

    target_country = countries[i] # get string of country
    sub_df = df_country.loc[df_country[col_name] == target_country] # specific row corresponding to target_country
    values = sub_df[column_list].values[0] # get values from each column in column_list
    trace = (dict(labels=labels,
                 values=values,
                 type='pie',
                 visible=visible))
    country_data.append(trace)

##

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

layout = html.Div([
        html.Div(html.Label('Subpage: '),style={'display': 'inline-block', 'vertical-align':'top','font-size':'20px'}),
        html.Div(dcc.Dropdown(
                    id='link_dropdown',
                    options=[{'label': links[i]['name'], 'value': i} for i in range(len(links))],
                    value=0),style={'display': 'inline-block', 'width': '30%'}),
        html.Div(dcc.Link(f"Go",id='link_visa_page', href=f"{links[0]['href']}"),style={'display': 'inline-block', 'width': '40%', 'vertical-align':'top', 'font-size':'20px'}),
    
        html.H1(children='2019 Visa Type Decomposition'),

        html.Div(children='''
            Visa types for international travel to the U.S., broken down by type.
        '''),
       
        # left dropdown
        html.Div([
            html.Label('Region'),
            dcc.Dropdown(
                id='region',
                options=[{'label': world_regions[i], 'value': i} for i in range(len(world_regions))],
                value=0)
            ], style={'display': 'inline-block', 'width': '40%', 'padding-right':'150px'}
        ),
       
        # right dropdown
        html.Div([ 
            html.Label('Country'),
            dcc.Dropdown(
                id='country',
                options=[{'label': countries[i], 'value': i} for i in range(len(countries))],
                value=0)
            ], style={'display': 'inline-block', 'width': '40%'}
        ),
        
        # left pie chart
        html.Div(
            dcc.Graph(
                id='pie-chart1',
                figure={
                    'data': region_data,
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }), style={'display': 'inline-block', 'width': '49%'}
        ),

        # right pie chart
        html.Div(
            dcc.Graph(
                id='pie-chart2',
                figure={
                    'data': country_data,
                    'layout': {
                        'title': 'Countries'
                    }
                }), style={'display': 'inline-block', 'width': '49%'}
        )
    ]
)

# control left pie chart (region)
@app.callback(
    dash.dependencies.Output('pie-chart1', 'figure'),
    [dash.dependencies.Input('region', 'value')])
def update_region_graph(region):
    for i in range(len(world_regions)):
        if i == region: region_data[i]['visible']=True
        else: region_data[i]['visible']=False
    return {
        'data': region_data,
        'layout': {
                'title': world_regions[region]
            }
    }

# control right pie chart (country)
@app.callback(
    dash.dependencies.Output('pie-chart2', 'figure'),
    [dash.dependencies.Input('country', 'value')])
def update_country_graph(country):
    for i in range(len(countries)):
        if i == country: country_data[i]['visible']=True
        else: country_data[i]['visible']=False
    return {
        'data': country_data,
        'layout': {
                'title': country_data[country]
            }
    }

@app.callback(
    Output('link_visa_page', 'href'),
    [Input('link_dropdown', 'value')])
def display_value(value):
    return links[value]['href']

if __name__ == '__main__':
    app.run_server(debug=True)