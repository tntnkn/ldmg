from dash import Dash, html

def init_dash(server):

    with server.app_context():
        from flask import render_template, redirect, url_for
        @server.route('/graph/')
        def graph():
            return render_template(
                    'graph.html',
                    footer=get_footer())

        @server.route('/graph/<path:path>')
        def graph_redirect(path):
            return redirect( url_for('/graph/') )

    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/graph/',
    )

    dash_app.layout = html.Div(
        id='dash-container',
        children=[
            html.H1(children='Hello Dash'),
            html.Div(children='''
                Dash: A web application framework for your data.
            '''),
        ]
    )
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pprint = pp.pprint

    def get_footer():
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(dash_app.index(), 'html.parser')
        footer = soup.footer
        return footer

    '''
    pprint(dash_app.index()) 

    pprint(footer)
    '''

    pprint(dir(dash_app))

    pprint(dash_app.routes)
    pprint(dash_app.index_string)

    return dash_app.server

