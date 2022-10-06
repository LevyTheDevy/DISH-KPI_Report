from dash import dcc, html
import dash_bootstrap_components as dbc

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    dcc.Loading(
        id="loading-1",
        type="default",
        children=html.Div(id='output-data-upload')
    ),
    dcc.Loading(
        id="loading-7",
        type="default",
        children=html.Div(id='output-data-message')
    ),
    html.Div(id='output-data-upload-settings'),
])

DISH_LOGO = ".assets\logo.png"

navbar = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="https://www.linkpicture.com/q/logo_56.png", height="30px")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="index",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.DropdownMenu(direction="start",
                                 children=[
                                     dbc.DropdownMenuItem("Home", href="index"),
                                     dbc.DropdownMenuItem("Upload", href="/apps/Upload")
                                 ],
                                 nav=True,
                                 in_navbar=True,
                                 label="More",
                                 ),
            ]
        ),
        color="dark",
        dark=True,
    )
])
