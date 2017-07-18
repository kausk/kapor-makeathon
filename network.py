import plotly
import plotly.plotly as py
from plotly.graph_objs import *

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

print __version__ # requires version >= 1.9.0

import networkx as nx

import random


## Names
names = ['Raphael', 'Sisi', 'Rob', 'Caroline', 'Willy', 'Anand', 'Dana', 'Noa', 'Takashi', 'Ethan', 'Kenny', 'Michael']
landlordNames = ['Becca', 'Joe', 'Ali', 'Gavin', 'Adam', 'Reid', 'Dan']
propertyNames = ["West Av.", "Summit St.", "Laurel Dr.", "Hudson St.", "Country Ln.", "Elizabeth St."]
communityCoins = ["Community Lessons", "Environmentally Conscious", "Maintenance"]
relatedCoin = ["Volunteering at Library", "Community Mentorship", "School Volunteering", "Community Outreach", "Safety Standards"]

## import graph
G=nx.random_geometric_graph(60,0.2)
landlords = random.sample(G.nodes(), 7)
#print(landlords)

tenants = []
for edge in G.edges():
    if edge[0] in landlords:
        tenants.append(edge[1])
    if edge[1] in landlords:
        tenants.append(edge[0])

coins = []
for edge in G.edges():
    if edge[0] in tenants and (edge[1] not in landlords):
        coins.append(edge[1])
    if edge[1] in tenants and (edge[0] not in landlords):
        coins.append(edge[1])

print(coins)




pos=nx.get_node_attributes(G,'pos')
## randomly scatter the node
dmin=1
ncenter=0
for n in pos:
    x,y=pos[n]
    d=(x-0.5)**2+(y-0.5)**2
    if d<dmin:
        ncenter=n
        dmin=d
p=nx.single_source_shortest_path_length(G,ncenter)



## create edge
edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines'
    )

for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        colorscale='Picnic',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2))
    )


for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

for node, adjacencies in enumerate(G.adjacency_list()):
    if node in landlords:
        node_trace['marker']['color'].append("red")
        node_info = 'Landlord Name: ' + random.sample(landlordNames, 1)[0] + '\nProperty: ' + random.sample(propertyNames, 1)[0] + '\nAvailable Units: ' + str(random.randint(0, 20))
        node_trace['text'].append(node_info)
    elif node in tenants:
        ## could be a color or a number
        node_trace['marker']['color'].append("blue")
        node_info = 'Tenant Name: ' + random.sample(names, 1)[0]
        node_trace['text'].append(node_info)
    elif node in coins:
        node_trace['marker']['color'].append("yellow")
        node_info = 'Coin earned for: ' + random.sample(communityCoins, 1)[0]
        node_trace['text'].append(node_info)
    else:
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = 'Related Coin: ' + random.sample(relatedCoin, 1)[0]
        node_trace['text'].append(node_info)     




fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Housing Graph of Community Members',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

plotly.offline.plot(fig, filename='networkx')