from werkzeug.contrib.profiler import ProfilerMiddleware
from pecbrasil import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [10])
app.run(debug = True)