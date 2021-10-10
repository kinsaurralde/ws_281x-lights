import plotly
from dash.dependencies import Output,Input


def register_callbacks_rtt(dashapp, getData):
    @dashapp.callback(Output('live-update-graph-bar', 'figure'),
              [Input('interval-component', 'n_intervals')])
    def update_rtt_graph(n_intervals):
        traces = getData()
        layout = plotly.graph_objs.Layout(xaxis={'title': 'Time'}, yaxis={'title': 'rtt (ms)'})
        return {'data': traces, 'layout': layout}
