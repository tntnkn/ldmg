#TODO:
#   1) convert strings to enums;
#   2) replace string exceptions to normal ones;
#   3) derive execptions from Exception;


from typing     import Dict

def addClasses(element: Dict):
    match element['value']['type']:
        case TransitionType.REGULAR_TEXT:
            element['classes'] += 'regular_text ' 
        case TransitionType.REGULAR_FIELD:
            element['classes'] += 'regular_field ' 
        case TransitionType.DYNAMIC_FIELD:
            element['classes'] += 'dynamic_field ' 
        case TransitionType.SINGLE_CHOICE:
            element['classes'] += 'single_choice ' 
        case TransitionType.MULTI_CHOICE:
            element['classes'] += 'multi_choice ' 
        case TransitionType.DOCUMENT:
            element['classes'] += 'document ' 
        case _:
            pass


from TableLoader    import load_tables, process_states_records, process_transitions_records
from Graph          import Graph


from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto

app = Dash(__name__)


states_records, transition_records = load_tables()
states = process_states_records(states_records)
transitions = process_transitions_records(transition_records)

graph = Graph(states, transitions)

def main():
    global graph

    print('\n')
    for node in graph.impl['elements']['nodes']:
        print(node, '\n')
    print('\n')
    for edge in graph.impl['elements']['edges']:
        print(edge, '\n')



###### DASH APP

###--- MAKE DASH APP

    main_title  = html.H1(
        id='main-title',
        children='Test Dash App',
        style={
            'border'            : 'thin solid black',
        }
    )

    roots = ''
    for n_id in graph.always_reachable_nodes_ids:
        roots += f"#{n_id}," 
    roots = roots[0:-1]
    print(roots)
    cytograph   = cyto.Cytoscape(
        id='graph_impl',
        layout={
            'name': 'breadthfirst',
            'roots': roots,
            'directed': True,
            'avoidOverlap': True,
        },
        style={
            'border'            : 'thin solid magenta',
            'height'            : '500px',
            'width'             : '75%',
            'background-color'  : '#D3D3D3',
        },
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'label'             : 'data(label)',
                    'text-opacity'      : 0.5,
                    'font-size'         : 10,
                    'curve-style'       : 'bezier',
                    'target-arrow-shape': 'triangle',
                }
            },
            {
                'selector': '.start_node',
                'style': {
                    'shape':    'star',
                }
            },
            {
                'selector': '.end_node',
                'style': {
                    'shape':    'round-diamond',
                }
            },
            {
                'selector': '.always_reachable_node',
                'style': {
                    'shape':    'round-pentagon',
                }
            },
            {
                'selector': '.regular_text',
                'style': {
                    'target-arrow-color': '#F08080',
                    'line-color': '#F08080'
                }
            },
            {
                'selector': '.regular_field',
                'style': {
                    'line-color': '#20B2AA',
                    'target-arrow-color': '#20B2AA',
                }
            },
            {
                'selector': '.dynamic_field',
                'style': {
                    'line-color': '#778899',
                    'target-arrow-color': '#778899',
                }
            },
            {
                'selector': '.single_choice',
                'style': {
                    'line-color': '#FAFAD2',
                    'target-arrow-color': '#FAFAD2',
                }
            },
            {
                'selector': '.multi_choice',
                'style': {
                    'line-color': '#90EE90',
                    'target-arrow-color': '#90EE90',
                }
            },
            {
                'selector': '.document',
                'style': {
                    'line-color': '#0000FF',
                    'target-arrow-color': '#0000FF',
                }
            },
            {
                'selector': '.default',
                'style': {
                    'line-color': '#00FFFF',
                    'target-arrow-color': '#00FFFF',
                }
            },
            {
                'selector': '.always_reachable',
                'style': {
                    'label': '',
                    'target-arrow-color': '#DCDCDC',
                    'line-color': '#DCDCDC',
                    'line-style': 'dashed',
                    'width'     : 1,
                }
            },
        ],
        elements=graph.impl['elements'],
    )

    graph_info  = html.Div(
        id='graph_info',
        children='test graph_info children',
        style={
            'border'            : 'thin solid red',
            'width'             : '25%',
        }
    )

    graph_area  = html.Div(
        id='graph_area',
        children=[
            graph_info, cytograph
        ],
        style={
            'display'           : 'flex',
            'flex-direction'    : 'row',
            'border'            : 'thin solid black',
        }
    )
    
    footer    = html.Div(
        id='footer',
        children='This is a footer.',
        style={
            'border'            : 'thin solid red',
        }
    )



    main_page   = html.Div(
        id='main-screen',
        children=[
            main_title,
            graph_area,
            footer
        ],
        style={
            'display'           : 'flex',
            'flex-direction'    : 'column',
            'width'             : '100%',
            'heigth'            : '100%',
            'border'            : 'thin solid blue',
        }
    )

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
