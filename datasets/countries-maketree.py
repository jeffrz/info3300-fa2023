# This is an example file -- intended for reference only
# It does not follow the best coding practices and is not the most efficient

import json, pprint

with open('countries-2016.json') as f:
    dat = json.loads( f.read() )
    
# eventually we will use root as the topmost node
root = {'name': 'World', 'population': 0, 'leaves': [] }
regions = {}
subregions = {}
countries = {}


for countryData in dat:
    regionName = countryData['region']
    subregionName = countryData['subregion']
    countryName = countryData['name']
    population = countryData['population']
    
    # -- start to "roll up" the country --
    
    # if we have a new region, add it to the root
    if regionName not in regions:
        region = { 'name': regionName, 'population': 0, 'leaves': [] }
        regions[regionName] = region
        root['leaves'].append(region)
    else:
        region = regions[regionName]
        
    # if we have a new subregion, add it to the region
    if subregionName not in subregions:
        subregion = { 'name': subregionName, 'population': 0, 'leaves': [] }
        subregions[subregionName] = subregion
        region['leaves'].append(subregion)
    else:
        subregion = subregions[subregionName]
        
    
    # create a leaf node for the country
    country = {'name': countryName, 'population': population, 'leaves': [] }
    
    # percolate up the country population
    subregion['leaves'].append(country)
    subregion['population'] += population
    region['population'] += population
    root['population'] += population
    

pprint.pprint( root )
        
        
        
        
        
        
        
