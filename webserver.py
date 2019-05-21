import app
from waitress import serve

# Arguments: host=(hostname),  port=(port to listen),  listen=(hostname:port to listen)  
#
serve(app.app, listen='127.0.0.1:8080')