import app
from waitress import serve

# Arguments: host=(hostname),  port=(port to listen),  listen=(hostname:port to listen)  
#
localhost = '127.0.0.1:8000'  # locally host the server
network_host = '0.0.0.0:8080' # host the server using PC's ip inside a network

if __name__ == '__main__':
  serve(app.app, listen=network_host)