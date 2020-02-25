import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, links
import pandas as pd

country_entry=pd.read_csv('./data/country_entries.csv')
slist =['China, PRC','Brazil','Japan','South Korea','India']
selected = country_entry[country_entry['Country'].isin(slist)]
selected = selected.sort_values(['Country','date'])

# reorganize data to graph separate traces
country_entry_data={}
for country in slist:
    entry=list(selected[selected['Country']==country]['entry'].values)
    date=list(selected[selected['Country']==country]['date'].values)
    country_entry_data[country]={'entry': entry, 'date':date}


layout = html.Div([
  html.Div(html.Label('Subpage: '),style={'display': 'inline-block', 'vertical-align':'top','font-size':'20px'}),
  html.Div(dcc.Dropdown(
              id='link_dropdown',
              options=[{'label': links[i]['name'], 'value': i} for i in range(len(links))],
              value=0),style={'display': 'inline-block', 'width': '30%'}),
  html.Div(dcc.Link(f"Go",id='link_travel', href=f"{links[0]['href']}"),style={'display': 'inline-block', 'width': '40%', 'vertical-align':'top', 'font-size':'20px'}),

  dcc.Graph(
    figure=dict(
      data=[
        dict(x=country_entry_data[country]['date'], 
             y=country_entry_data[country]['entry'],
             name=country
             ) for country in slist
             ],
    layout=dict(
      title="Monthly Entry to the U.S. by Country",
      showlegend=True,
      xaxis=dict(title='Time (by month)'),
      yaxis=dict(title='Number of Entries')
    ))
  )
])

@app.callback(
    Output('link_travel', 'href'),
    [Input('link_dropdown', 'value')])
def display_value(value):
    return links[value]['href']