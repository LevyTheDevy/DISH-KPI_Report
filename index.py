from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import LEVI_Black_White, LEVI_Image_Collage


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="index")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Image to Black & White", href="/apps/LEVI_Black_White"),
                    dbc.DropdownMenuItem("Image Collage", href="/apps/LEVI_Image_Collage"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="LEVI",
        brand_href="index",
        color="primary",
        dark=True),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/LEVI_Black_White':
        return LEVI_Black_White.layout
    if pathname == '/apps/LEVI_Image_Collage':
        return LEVI_Image_Collage.layout
    else:
        return "index"


if __name__ == '__main__':
    app.run_server(debug=True)
