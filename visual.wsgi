import sys
sys.path.insert(0, '/home/politica/git/pecbrasil/')

from pecbrasil import app as application

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(application, True)
