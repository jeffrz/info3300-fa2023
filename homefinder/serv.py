
# If this code does not work, make sure that you've installed Flask
# This code should work in both Python 2 and 3
from flask import *
import json, csv
from pprint import pprint


app = Flask(__name__, static_url_path='/static')

# Root path serves up index.html from the static directory -- we'll be editing this for the d3 part of the lecture
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
    

# Main app used to interface with the flask library
# Decorators will make use of this, but in many cases we will call
#  functions straight from flask such as send_from_directory and jsonify
app = Flask(__name__, static_url_path='')  # By default, looks in ./static

# Root path serves up index.html from the static directory -- we'll be editing this for the d3 part of the lecture
@app.route('/')
def index():
    return app.send_static_file('index.html')

# For the CSS files, take in part of the path as a variable to use
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)    
    
    
# Import topoJSON data to serve to client
map = {}
with open('pittsburgh_neighborhoods.json') as f:
    map = json.load( f )
    
@app.route('/map')
def pghmap():
    return jsonify( map )    

# jsonify is a built-in flask command that creates a JSON response out of most Py objects    
    
    
# Make a flat dictionary "database" for our use -- this should be not be used in a production system
# Pick a more resilient option (or even just SQLite) if you're going to try this in practice

db = {}
# HouseID => {'HouseID','Neighborhood','Latitude','Longitude','Lot Size','Finished Size','Sale Price','Year Built','Bathrooms','Bedrooms','Description'}
with open('pgh_homes.json') as f:
    homes = json.load( f ) 
    for home in homes:  #python for X in Y iterates like Y.forEach( x => {stuff} ) in JS
        db[ home['HouseID'] ] = home


# Serve a list of houses to the client in JSON form
# outputKeys specifies the specific keys of data we're going to send to the client
# The intuition here is that we don't want to waste bandwidth sending fields the client may not need at the start, like Description
outputKeys = ['HouseID','Neighborhood','Latitude','Longitude','Sale Price','Bathrooms','Bedrooms','Lot Size']

# OLD VERSION OF HOUSES ENDPOINT
# @app.route('/houses')
# def houses():
#     houses = []
#     for homeID in db: 
#         home = db[homeID]
#         outputHome = { key: home[key] for key in outputKeys }
#         houses.append(outputHome)
#     return jsonify(houses)

# NEW VERSION THAT USES URL PARAMETERS
# Houses will enable filtering through URL query parameters (https://skorks.com/2010/05/what-every-developer-should-know-about-urls/)
@app.route('/houses')
def houses():    
    # Fetch filter criteria from URL params  (None if not present or not float)
    priceMin = request.args.get('priceMn', None, type=float)
    priceMax = request.args.get('priceMx', None, type=float)
    bathMin = request.args.get('bathMn', None, type=float)
    bathMax = request.args.get('bathMx', None, type=float)
    bedMin = request.args.get('bedMn', None, type=float)
    bedMax = request.args.get('bedMx', None, type=float)
    
    # Create a new array of houses to send to client
    filtered = []
    for home in db.values(): # iterate through values in the dictionary
        
        # Apply filter criteria, if the user included them in their request
        # There are fancier, more Pythonic ways to do this, but some ifs is quick for a demo app
        # After all, in reality this would be implemented in a database query because you won't be using
        #  a flat dictionary object as your database in a production system! Don't do it!
        if priceMin is not None and home['Sale Price'] < priceMin:
            continue
        if priceMax is not None and home['Sale Price'] > priceMax:
            continue
        if bathMin is not None and home['Bathrooms'] < bathMin:
            continue
        if bathMax is not None and home['Bathrooms'] > bathMax:
            continue
        if bedMin is not None and home['Bedrooms'] < bedMin:
            continue
        if bedMax is not None and home['Bedrooms'] > bedMax:
            continue
        
        # Only send the outputKeys we specified
        outputHome = { key: home[key] for key in outputKeys }
        filtered.append(outputHome)
        
    return jsonify( filtered )

# Provide the entire row of data for a house when the client specifies a HouseID
# Return an error if the HouseID is invalid
@app.route('/details')
def details():
    ident = request.args.get("id", None, type=int)
    
    if ident is None:
        response = make_response("No ID")
        response.status_code = 400 # code 400 is a Bad Request code
        return response
    else:
        if ident not in db:
            response = make_response("ID not in database")
            response.status_code = 400
            return response
        else:
            return jsonify( db[ident] )   # wrap this house's data in JSON and send
    
    # never will reach here
    return make_response("")


# We want to give clients a mechanism to "star" or mark their favorite houses
# Ideally this will last between multiple sessions (reloads) of the page
# Here we store everything in memory, which means the starred items will be lost if the server is closed
# In practice you'd implement this using a mix of user accounts, cookies, and a database

# Return JSON list of starred HouseIDs
starredItems = set()
@app.route('/starred')
def starred():
    return jsonify( list(starredItems) )

# Star a new HouseID and return a JSON list of starred HouseIDs
@app.route('/star')
def star():
    ident = request.args.get("id", None, type=int)
    
    if ident is None:
        response = make_response("No ID")
        response.status_code = 400
        return response
    else:
        if ident not in db:
            response = make_response("ID not in database")
            response.status_code = 400
            return response
        else:
            if ident in starredItems:
                return jsonify( list(starredItems) )
                
            starredItems.add(ident)
            return jsonify( list(starredItems) )
    
    # never will reach here
    return make_response("")

# Unstar a HouseID and return a JSON list of starred HouseIDs
@app.route('/unstar')
def unstar():
    ident = request.args.get("id", None, type=int)
    
    if ident is None:
        response = make_response("No ID")
        response.status_code = 400
        return response
    else:
        if ident not in db:
            response = make_response("ID not in database")
            response.status_code = 400
            return response
        else:
            if ident in starredItems:
                starredItems.remove(ident)
                
                return jsonify( list(starredItems) )
                
            return jsonify( list(starredItems) )

      
    
    
# DO NOT DO THIS IN A PRODUCTION ENVIRONMENT
# ARGUABLY, THIS IS EVEN A BAD THING FOR DEVELOPING WITH FLASK
# You should never expose dev servers to the public
# Always use a bridge with a real web server if you're doing this
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9999')
    
    
    
