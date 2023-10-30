
# If this code does not work, make sure that you've installed Flask
# This code should work in both Python 2 and 3
from flask import *
import json, csv

app = Flask(__name__, static_url_path='')







# HouseID => {'HouseID','Neighborhood','Latitude','Longitude','Lot Size','Finished Size','Sale Price','Year Built','Bathrooms','Bedrooms','Description'}


    

outputKeys = ['HouseID','Neighborhood','Latitude','Longitude','Sale Price','Bathrooms','Bedrooms','Lot Size']


    
    
    
    
# DO NOT DO THIS IN A PRODUCTION ENVIRONMENT
# ARGUABLY, THIS IS EVEN A BAD THING FOR DEVELOPING WITH FLASK
# You should never expose dev servers to the public
# Always use a bridge with a real web server if you're doing this
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9999')
    
    
    
