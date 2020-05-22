#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import pandas as p

#,df,propindex=None
    
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):        
        request_path = self.path[1:].replace('+',' ')
        self.send_response(200)
        #self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()
        print("Request path:", request_path)
        global colindex,df,valindex
        #print(df.columns)
        #print(df[propindex])
        results=df[df[propindex].str.contains(request_path,na=False)]
        if len(results)>1:
            self.wfile.write(str(results[valindex]).encode("utf-8"))
        elif len(results)==0:
            self.wfile.write('NOT FOUND. Check Spelling'.encode("utf-8"))
        else:    
            val=results.iloc[0][valindex]
            self.wfile.write(val.encode("utf-8"))

def main():
    global df,csv,propindex
    df=p.read_csv(csv, header=None)
    #print(df.head())
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
    #global csv,propindex
    print(args)
    csv=args[0]
    propindex=int(args[1])
    valindex=int(args[2])
    main()
