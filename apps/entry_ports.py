import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, links
import pandas as pd

df = pd.read_excel('./data/port_of_entry.xlsx', sheet_name='Percent Change', header=1)
df = df.rename(columns={'TOP 30 Ports of Entry': 'Ports of Entry','2012\n': '2012', '2013\n': '2013','2014\n': '2014','2015\n': '2015','2016\n': '2016','2017\n': '2017','2018\n': '2018'})
port_names=df['Ports of Entry']
port_id=0
df_city = pd.DataFrame(data=df.iloc[port_id,:])
percent_change=list(df_city[0])[1:]
year = ['2012', '2013', '2014', '2015', '2016', '2017', '2018']
for i in range(len(percent_change)):
    percent_change[i] = float(percent_change[i])

port_data=[dict(x=year,
                  y=percent_change,
                  name='Percent Change',
                  type='bar')]


layout = html.Div([
    html.Div(html.Label('Subpage: '),style={'display': 'inline-block', 'vertical-align':'top','font-size':'20px'}),
  html.Div(dcc.Dropdown(
              id='link_dropdown',
              options=[{'label': links[i]['name'], 'value': i} for i in range(len(links))],
              value=0),style={'display': 'inline-block', 'width': '30%'}),
  html.Div(dcc.Link(f"Go",id='link_port', href=f"{links[0]['href']}"),style={'display': 'inline-block', 'width': '40%', 'vertical-align':'top', 'font-size':'20px'}),
    
  html.Div([ 
            html.Label('Port of Entry'),
            dcc.Dropdown(
                id='city_dropdown',
                options=[{'label': port, 'value': i} for i,port in enumerate(df['Ports of Entry'].values)],
                value=0)
            ], style={'display': 'inline-block', 'width': '40%'}
        ),
  dcc.Graph(
    id='bar_graph',
    figure={
      'data':port_data,
      'layout':{
        'title':'YoY Percent Change of Foreign Arrivals by Port - New York, NY'
      }
    }
  )
])

@app.callback(
    dash.dependencies.Output('bar_graph', 'figure'),
    [dash.dependencies.Input('city_dropdown', 'value')])
def update_port_graph(port):  
  port_name=port_names[port]
  df_city = pd.DataFrame(data=df.iloc[int(port),:])

  percent_change=list(df_city[port])[1:]
  year = ['2012', '2013', '2014', '2015', '2016', '2017', '2018']
  for i in range(len(percent_change)):
      percent_change[i] = float(percent_change[i])
  port_data=[dict(x=year,
                  y=percent_change,
                  name='Percent Change',
                  type='bar')]
  return {
      'data':port_data,
      'layout':{
        'title':f'YoY Percent Change of Foreign Arrivals by Port - {port_name}',
        'xaxis':dict(title="Year"),
        'yaxis':dict(title="YoY Percent Change")
      }
  }

@app.callback(
    Output('link_port', 'href'),
    [Input('link_dropdown', 'value')])
def display_value(value):
    return links[value]['href']
    
if __name__ == '__main__':
    app.run_server(debug=True)