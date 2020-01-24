#!/usr/bin/env python3
from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app, socketio

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
socketio.run(app, debug = True, port=200)
