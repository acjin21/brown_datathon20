import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
links=[
  {'name': 'Visa Type Decomposition' ,'href':'/apps/visa_type'},
  {'name': 'Coronavirus Details' ,'href':'/apps/corona'},
  {'name': 'Travel by Nationality' ,'href':'/apps/travel_volume'},
  {'name': 'Ports of Entry', 'href':'/apps/entry_ports'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True