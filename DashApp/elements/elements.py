from dash       import html, dcc
import dash_cytoscape as cyto
from ..static   import styles


main_title  = html.H1(
    id='main-title',
    children='Test Dash App',
    style=styles.main_title_style,
)


cytograph   = cyto.Cytoscape(
    id='graph_impl',
    layout={
        'name': 'breadthfirst',
        'directed': True,
        'avoidOverlap': True,
    },
    style=styles.graph_style,
    stylesheet=styles.graph_stylesheet,
)


graph_info  = html.Div(
    id='graph_info',
    children='test graph_info children',
    style=styles.graph_info_style,
)


graph_area  = html.Div(
    id='graph_area',
    children=[
        graph_info, cytograph
    ],
    style=styles.graph_area_style,
)


footer    = html.Div(
    id='footer',
    children='This is a footer.',
    style=styles.footer_style,
)


main_page   = html.Div(
    id='main-screen',
    children=[
        main_title,
        graph_area,
        footer
    ],
    style=styles.main_page_style
)

