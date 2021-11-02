import time

import dashapp.callbacks
import dashapp.layout

import random
import plotly


packet_manager = None

def setup(app, metrics_dashboard, pm):
    with app.app_context():
        global packet_manager
        packet_manager = pm
        metrics_dashboard.title = 'Metrics'
        metrics_dashboard.layout = dashapp.layout.layout
        dashapp.callbacks.register_callbacks_rtt(metrics_dashboard, getRTTData)


def formatTimestampToSecondsAgo(timestamps):
    result = []
    now = int(time.time() * 1000)
    for timestamp in timestamps:
        result.append(f"-{(now - timestamp) / 1000}s")
    return result

def getRTTData():
    data = packet_manager.stats.filterRecentNSecs("rtt", 15)
    traces = list()
    for t in data:
            traces.append(plotly.graph_objs.Scatter(
                x=formatTimestampToSecondsAgo(data[t]['x']),
                y=data[t]['y'],
                name='IP: {}'.format(t)
                ))
    return traces