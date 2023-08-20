import json, sys
from pprint import pprint

# takes in titanic.json and produces a directed acyclic graph for sankey diagramming

with open('titanic.json') as f:
    dat = json.loads( f.read() )
    


def ageQuartile( age ):
    if age < 21:
        return 'Age - 1st Quartile'
    elif age < 28:
        return 'Age - 2nd Quartile'
    elif age < 38:
        return 'Age - 3rd Quartile'
    else:
        return 'Age - 4th Quartile'

# diagram
#  age quartile -> mortality -> cabin class -> sex 

nodes = []
nodesByName = {}
def getNode(name):
    if name in nodesByName:
        node = nodesByName[name]
    else:
        node = {'id': len(nodes),
                'name': name }
        nodes.append(node)
        nodesByName[name] = node
    return node

ageVals = {}
sexVals = {}
classVals = {}
mortalityVals = {}
for element in dat:
    ageq = ageQuartile(element['age'])
    s = element['sex']
    c = element['class']
    m = element['mortality']
    
    ageVals[ageq] = ageVals.get(ageq,[])
    ageVals[ageq].append(element)
    sexVals[s] = sexVals.get(s,[])
    sexVals[s].append(element)
    classVals[c] = classVals.get(c,[])
    classVals[c].append(element)
    mortalityVals[m] = mortalityVals.get(m,[])
    mortalityVals[m].append(element)

map(getNode, sorted(ageVals.keys()) ) 
map(getNode, sorted(mortalityVals.keys()) )
map(getNode, sorted(classVals.keys()) )
map(getNode, sorted(sexVals.keys()) )

edges = []

#  age -> mortality
for age in ageVals:
    nodeSrc = getNode(age)
            
    counts = {}
    for element in ageVals[age]:
        m = element['mortality']
        counts[m] = counts.get(m, 0) + 1
    
    for mort in counts:
        nodeTgt = getNode(mort)

        edges.append( { 'source': nodeSrc['id'],
                        'target': nodeTgt['id'],
                        'name': '%s - %s' % (nodeSrc['name'], nodeTgt['name']),
                        'value':  counts[mort] } )

#  mortality -> class
for mort in mortalityVals:
    nodeSrc = getNode(mort)
            
    counts = {}
    for element in mortalityVals[mort]:
        c = element['class']
        counts[c] = counts.get(c, 0) + 1
    
    for c in counts:
        nodeTgt = getNode(c)

        edges.append( { 'source': nodeSrc['id'],
                        'target': nodeTgt['id'],
                        'name': '%s - %s' % (nodeSrc['name'], nodeTgt['name']),
                        'value':  counts[c] } )

#  class -> sex
for c in classVals:
    nodeSrc = getNode(c)
            
    counts = {}
    for element in classVals[c]:
        s = element['sex']
        counts[s] = counts.get(s, 0) + 1
    
    for s in counts:
        nodeTgt = getNode(s)

        edges.append( { 'source': nodeSrc['id'],
                        'target': nodeTgt['id'],
                        'name': '%s - %s' % (nodeSrc['name'], nodeTgt['name']),
                        'value':  counts[s] } )

print json.dumps( {'nodes': nodes,
                   'links': edges } )
