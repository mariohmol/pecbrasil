from pecbrasil import app

from flask.ext.script import Manager,Server
manager = Manager(app)
manager.add_command("runserver", Server(port=8084, host='0.0.0.0'))

manager.run()
