import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import visa_type, corona, travel_volume, entry_ports


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/visa_type':
        return visa_type.layout
    elif pathname == '/apps/corona':
        return corona.layout
    elif pathname == '/apps/travel_volume':
        return travel_volume.layout
    elif pathname == '/apps/entry_ports':
        return entry_ports.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
