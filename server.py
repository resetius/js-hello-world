import time
import BaseHTTPServer
import mysql.connector
import json

HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.

cnx=mysql.connector.connect(user="user",password="password",host="localhost",database="test")

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        
    def do_POST(s):
        l=int(s.headers.getheader('content-length'))
        content=s.rfile.read(l)

        message=json.loads(content)

        cursor = cnx.cursor()
        query="INSERT INTO messages (name, body) VALUES (%(name)s, %(body)s)"
        cursor.execute(query, message)
        cnx.commit()
        cursor.close()
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write("{}")

    def do_GET(s):
        """Respond to a GET request."""
        if s.path == "/messages":
            s.get_messages()
            return

        fname = s.path.split('/')[-1]
        with open(fname, "r") as file:        
            s.send_response(200)
            if fname.endswith(".html"):
                s.send_header("Content-type", "text/html")
            else:
                s.send_header("Content-type", "text/javascript")
            s.end_headers()
            s.wfile.write(file.read())

    def get_messages(s):
        cursor = cnx.cursor()

        cursor.execute("SELECT * from messages")

        answer=[]

        for (_id, parent_id, name, body) in cursor:
            answer += [{'id': _id, 'parent_id': parent_id, 'name': name, 'body': body}]

        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()

        s.wfile.write(json.dumps(answer))

        cursor.close()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
    
