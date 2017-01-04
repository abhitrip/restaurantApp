from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
class webserverHandler(BaseHTTPRequestHandler):
    def getRestaurants(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        listOfRestaurants = session.query(Restaurant.name).all()
        res = []
        for rest in listOfRestaurants:
            res.append(rest[0])
        session.close()
        return '<br>'.join(res)

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello!</body></html>"
                output+= """<form method='POST' enctype='multipart/form-data'
                action='/hello'> <h2> What would u like to say?</h2>
                <input name='message' type='text'><input type='submit' value='Submit'>
                </form>
                """
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return
            elif self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body> &#161 Hola ! <</body></html>"
                output+= """<form method='POST' enctype='multipart/form-data'
                action='/hello'> <h2> What would u like to say?</h2>
                <input name='message' type='text'><input type='submit' value='Submit'>
                </form>
                """
                output+="</body></html>"
                self.wfile.write(output)
            elif self.path.endswith("/edit"):
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            elif self.path.endswith("/delete"):
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurantIDPath = self.path.split("/")[2]
                myRestQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestQuery:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output+= "<h1>"
                    output+= "Are u sure u wanna Delete the restaurant %s?" %myRestQuery.name
                    output+= "</h1>"
                    output+= """<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>'""" % restaurantIDPath
                    output+= "<input type = 'submit' value = 'Submit'>"
                    output+= '</form>'
                    output+= "</body></html>"
                    print output
                    self.wfile.write(output)

            elif self.path.endswith("/restaurants"):
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+= "<a href='/restaurants/new'> Add new restaurants here</a> <br><br>"
                listOfRestaurants = session.query(Restaurant.name).all()
                res = []
                for idx,rest in enumerate(listOfRestaurants):
                    # Obj1
                    output+= rest.name + "<br>"
                    # Obj2
                    output+= "<a href='restaurants/%s/edit'>EDIT</a><br>" % str(idx+1)
                    output+= "<a href='restaurants/%s/delete'>DELETE</a><br><br>" %str(idx+1)
                    output+= "</body></html>"
                session.close()

                print output
                self.wfile.write(output)



            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output=""
                output+= "<html><body>"
                output+= """<form method='POST' enctype='multipart/form-data'
                action='/restaurants/new'> <h2> Name of your restaurant</h2>
                <input name='rest' type='text'><input type='submit' value='Submit'>
                </form>
                """
                output+="</body></html>"
                self.wfile.write(output)

        except IOError:
            self.send_error(404,"File %s not found" %self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    msgContent = fields.get('rest')
                    restName = msgContent[0]
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()
                    newRestaurant = Restaurant(name=restName)
                    session.add(newRestaurant)
                    session.commit()
                    session.close()
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()


            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                print "Inside post",ctype
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)


                    messagecontent = fields.get('newName')

                    restaurantIDPath = self.path.split("/")[2].strip()
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    print myRestaurantQuery

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
            elif self.path.endswith("/delete"):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype=="multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    restaurantIDPath = self.path.split("/")[2].strip()
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery!=[]:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()



            elif self.path.endswith('/hello'):
                self.send_response(301)
                self.end_headers()
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messageContent = fields.get('message')
                output = ""
                output+= "<html><body>"
                output+= "<h2> Okay, How about this :</h2>"
                output+= "<h1> %s</h1>" % messageContent[0]
                output+= """<form method='POST' enctype='multipart/form-data'
                action='/hello'> <h2> What would u like to say?</h2>
                <input name='message' type='text'><input type='submit' value='Submit'>
                </form>
                """
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return
        except:
            pass

def main():
    try:
        port = 8080
        hostname = ''
        portNumber = 8080
        server = HTTPServer((hostname,portNumber),webserverHandler)
        print "Web server running on port %s" %portNumber
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stoppin web server....."
        server.socket.close()


if __name__ == '__main__':
    main()

