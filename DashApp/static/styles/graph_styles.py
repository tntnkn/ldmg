graph_stylesheet=[
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
            'shape':    'vee',
        }
    },
    {
        'selector': '.always_reachable_node',
        'style': {
            'shape':    'round-pentagon',
        }
    },
    {
        'selector': '.cond_edge',
        'style': {
            'line-color': '#FAFAD2',
            'target-arrow-color': '#FAFAD2',
        }
    },
    {
        'selector': '.uncond_edge',
        'style': {
            'line-color': '#90EE90',
            'target-arrow-color': '#90EE90',
        }
    },
    {
        'selector': '.always_reachable_edge',
        'style': {
            'label': '',
            'target-arrow-color': '#DCDCDC',
            'line-color': '#DCDCDC',
            'line-style': 'dashed',
            'width'     : 1,
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
        'selector': '.button',
        'style': {
            'line-color': '#FAFAD2',
            'target-arrow-color': '#FAFAD2',
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
]


graph_style = {
    'border'            : 'thin solid magenta',
    'height'            : '500px',
    'width'             : '75%',
    'background-color'  : '#D3D3D3',
}

