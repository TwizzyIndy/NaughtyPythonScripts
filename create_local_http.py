
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer

def createLocalServer() :
    
    PORT = 8000
    
    handler = SimpleHTTPRequestHandler
    server = BaseHTTPServer.HTTPServer
    
    protocol = "HTTP/1.0"
    sv_addr = ('127.0.0.1', PORT)
    
    handler.protocol_version = protocol
    
    httpd = server(sv_addr, handler)
    sa = httpd.socket.getsockname()
    
    
    print "serving at : " + str(httpd.server_address)
    httpd.serve_forever()
    
def main():
    createLocalServer()
    
if __name__ == "__main__":
    main()