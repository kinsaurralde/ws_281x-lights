import dash_core_components as dcc
import dash_html_components as html


layout = html.Div([
        html.H1('RTT'),
        html.Div([
            # html.Button("Pause", id="button_1"),
            # html.Button("Resume", id="button_2"),
            dcc.Graph(id='live-update-graph-bar', animate=False),
            dcc.Interval(
                id='interval-component',
                interval=5000
            )
        ])
    ], style={'width': '500'})


