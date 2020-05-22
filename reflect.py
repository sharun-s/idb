#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

f=open('names_found','r')
names=f.readlines()
f.close()
print(names[1])
rcount=1

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):        
        request_path = self.path[1:].replace('+',' ')
        self.send_response(200)
        #self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()
        print("Request path:", request_path)
        global rcount
        self.wfile.write(names[rcount].encode("utf-8"))
        rcount=rcount+1
        
def main():
    port = 8084
    print('Listening on 0.0.0.0:%s' % port)
    server = HTTPServer(('127.0.0.1', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    
    main()
