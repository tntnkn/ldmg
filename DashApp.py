#TODO:
#   1) replace string exceptions with normal ones;
#   2) derive execptions from Exception;

from Graph             import Loader
from DashApp           import CytoGraph
from DashApp.elements  import cytograph, main_page

from dash import Dash, Input, Output

app = Dash(__name__)

loader = Loader()
loader.load_graph()
graph = loader.graph

cgraph = CytoGraph(loader.graph) 

def main():
    global cgraph
    global loader

    print('\n')
    for node in cgraph.impl['elements']['nodes']:
        pass
        print('- ', node, '\n')
    print('===\n')
    for edge in cgraph.impl['elements']['edges']:
        pass
        print('- ', edge, '\n')


    roots = ''
    for n_id in graph.always_reachable_nodes_ids:
        roots += f"#{n_id}," 
    roots = roots[0:-1]
    
    cytograph.elements=cgraph.impl['elements']
    cytograph.layout['roots'] = roots


    app.layout   = main_page 
    app.run_server(debug=True)


import json
@app.callback(Output('graph_info', 'children'),
              Input('graph_impl', 'tapEdgeData'))
def displayTapEdgeData(data):
    if not data:
        return "Empty"
    global graph
    return graph.transitions[data['id']]['type'].value
    return json.dumps(data, indent=2)



if __name__ == '__main__':
    main()

