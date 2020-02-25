import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, links
import pandas as pd
import numpy as np

corona_file="./data/corona_daily.csv"
sars_file="./data/sars_daily.csv"

corona_df=pd.read_csv(corona_file)
sars_df=pd.read_csv(sars_file)

airline_df = pd.read_csv("./data/totaldff.csv")

### NEWS SOURCES API QUERY ###
import requests
import pandas as pd
url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'q=Coronavirus&'
       'from=2020-01-24&'
       'sortBy=popularity&'
       'apiKey=1abc60ef1ce04d22b846b9a90e68181e')

response = requests.get(url)
article_titles=([art['title'] for art in response.json()['articles']])
article_sources=([art['source']['name'] for art in response.json()['articles']])

data={'title':article_titles, 'source':article_sources}
news_df=pd.DataFrame(data, columns=['title', 'source'])
####
# Year-on-year
####
yearly_data=[[] for i in range(20)]
def get_year(str): return int(str.split('-')[1])
def get_month(str): return str.split('-')[0]

months=dict({'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'Jun':5,'Jul':6,'Aug':7,'Sep':8,'Oct':9,'Nov':10,'Dec':11})
for row in airline_df.values:
    date=row[0]
    count=row[1]
    m=months[get_month(date)]
    y=get_year(date)-2000
    yearly_data[y].append(count)

yoy_x=[]
yoy_data=[]
for i in range(1,19):
    yoy_data.append(np.array(yearly_data[i])/np.array(yearly_data[i-1])-1)


for y in range(2001,2019):
    for m in months.keys():
        yoy_x.append(m+"-"+str(y))
yoy_y = np.array(yoy_data).flatten()


layout = html.Div([
    
    html.Div(html.Label('Subpage: '),style={'display': 'inline-block', 'vertical-align':'top','font-size':'20px'}),
    html.Div(dcc.Dropdown(
                id='link_dropdown',
                options=[{'label': links[i]['name'], 'value': i} for i in range(len(links))],
                value=0),style={'display': 'inline-block', 'width': '30%'}),
    html.Div(dcc.Link(f"Go",id='link', href=f"{links[0]['href']}"),
            style={'display': 'inline-block', 'width': '40%', 'vertical-align':'top', 'font-size':'20px'}),
    
    html.Div(
        dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=corona_df['day'],
                        y=corona_df['confirmed'],
                        name='Corona Confirmed',
                        marker=dict(
                            color='red'
                        )
                    ),
                    dict(
                        x=corona_df['day'],
                        y=corona_df['deaths'],
                        name='Corona Deaths',
                        marker=dict(
                            color='blue'
                        )
                    ),
                    dict(
                        x=sars_df['day'],
                        y=sars_df['confirmed'],
                        name='SARS Confirmed',
                        marker=dict(
                            color='green'
                        )
                    ),
                    dict(
                        x=sars_df['day'],
                        y=sars_df['deaths'],
                        name='SARS Deaths',
                        marker=dict(
                            color='purple'
                        )
                    )
                ],
                layout=dict(
                    title='Corona vs SARS',
                    showlegend=True,
                    xaxis=dict(title='# Days Since Start of Outbreak'),
                    yaxis=dict(title='# Cases'),\
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            ),
            style={'height': 300},
            id='my-graph'
        ),style={'width': '45%', 'display': 'inline-block'}),

        html.Div([
        html.Label('Coronavirus Headline News'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in news_df.columns],
            data=news_df.to_dict('records'),
            style_table={
                'overflowX': 'scroll',
                'border': 'thin lightgrey solid',
                'padding': '5px'
             },
        )],style={'width': '50%', 'display': 'inline-block', 
        'float':'right', 'padding-right':'50px','textAlign': 'center', 
        'fontSize':'14px'}),

    html.Div(dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=list(airline_df['months'].values),
                    y=list(airline_df['sum'].values))
            ],
            layout=dict(title="Air Traffic from China/HK to U.S. Per Month",
            xaxis=dict(title="Month"),
            yaxis=dict(title="Number of Travelers"))
            )
        )
    ),

    html.Div(
        dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=yoy_x,
                    y=yoy_y)
            ],
            layout=dict(
                title="Year-on-Year Air Traffic From China/HK to U.S. Per Month",
                xaxis=dict(title="Month"),
                yaxis=dict(title="YoY"))

            )
        )
    )
])


@app.callback(
    Output('link', 'href'),
    [Input('link_dropdown', 'value')])
def display_value(value):
    return links[value]['href']