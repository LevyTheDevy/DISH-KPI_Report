import dash
import dash_auth
import dash_bootstrap_components as dbc

VALID_USERNAME_PASSWORD_PAIRS = {
    'ryan': 'dish',
    'nikhil': 'dish',
    'rohit': 'dish',
    'josh': 'dish',
    'levi': 'dish',
    'dish': 'dish2022',
}

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ], suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
'''auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)'''

# Main Server
app.title = 'DISH KPI Report'
app._favicon = ("icon.ico")
server = app.server

""""Protocol_FIG(data_market_DF, name), \
               DATA_FIG(data_market_DF, name), \
               VoNR_TECH_BAR_FIG(voice_market_DF, name), \
               VoNR_Result_MAP_FIG(voice_market_DF, name), \
               TECH_MAP_FIG(voice_market_DF, name), \
               Voice_HO_SINR_RSRP_BAR_FIG(voice_market_DF, name), \
               RSRP_MAP_FIG(voice_market_DF, name), \
               SINR_MAP_FIG(voice_market_DF, name), \""""


