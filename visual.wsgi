import sys
sys.path.insert(0, '/home/peclube/public_html/')
sys.executable = '/usr/bin/python2.7'

from pecbrasil import app as application

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(application, True)
