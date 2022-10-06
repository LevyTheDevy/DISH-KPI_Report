import base64
import datetime
import io
import random
from datetime import date
import dash
import dash_bootstrap_components as dbc
import gspread
import numpy as np
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from apps.Upload import navbar

# Todo Before deploy
# Todo HIGH: User output for no data in selected filter.
# Todo HIGH: Download .PDF graph report.
# Todo HIGH: Optimize speed and comment code.
# Todo MID: Update Graphs with Date Information.
# Todo LOW: Add LOGO/ICON/Page Title / Credits.

Data_KPI_REQ = ["TIME_STAMP", "GPS Lon", "GPS Lat", "Event Technology", "5G KPI PCell RF Serving SS-RSRP [dBm]",
                "5G KPI PCell RF Serving SS-SINR [dB]", "5G KPI Total Info Layer1 PDSCH Throughput [Mbps]",
                "5G KPI Total Info Layer1 PUSCH Throughput [Mbps]", "5G KPI PCell Layer1 DL BLER [%]",
                "5G KPI PCell Layer1 UL BLER [%]", "5G KPI PCell Layer1 DL MCS (Avg)",
                "5G KPI PCell Layer1 UL MCS (Avg)", "AutoCallSummary Status", "5G KPI PCell Layer1 RACH Reason",
                "5G KPI PCell Layer1 RACH Result", "5G KPI PCell RF Band", "5G KPI Total Info DL CA Type", "Market"]
Voice_KPI_REQ = ["TIME_STAMP", "GPS Lat", "GPS Lon", "Voice Call", "5G KPI PCell RF Serving SS-RSRP [dBm]",
                 "5G KPI PCell RF Serving SS-SINR [dB]", "Event Technology",
                 "5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverResult", "AutoCallSummary Status", "Market"]

from fig import Protocol_FIG, DATA_FIG, VoNR_TECH_BAR_FIG, VoNR_Result_MAP_FIG, TECH_MAP_FIG, \
    Voice_HO_SINR_RSRP_BAR_FIG, RSRP_MAP_FIG, SINR_MAP_FIG

gc = gspread.service_account(filename='assets/custom-producer-357322-a044a0660521.json')
sh = gc.open("KPI_DATA")

# Connect to main app.py file
from app import app
from app import server
# Connect to your app pages
from apps import Upload

fig_layout = dbc.Container([
    dbc.Row([
        # About and how to....
        dbc.Col([
            html.Div([
                html.H5("DISH KPI Report Tool"),
                html.P(
                    "This tool is used for uploading KPI data in different markets and analyzing it on a daily basis. You can upload new file by clicking on the dropdown menu and selecting upload"),
                html.Hr(),
                html.Div(id='Error-output')
            ], className='pt-3')
        ], width=6),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Select Date", className='pt-3'),
                        dcc.DatePickerSingle(
                            id='my-date-picker-single-report',
                            min_date_allowed=date(2022, 9, 20),
                            max_date_allowed=date(2023, 9, 20),
                            initial_visible_month=date.today(),
                            date=date.today()
                        ),
                    ])
                ]),
                dbc.Col([
                    html.P("Select Market", className='pt-3'),
                    dbc.Select(
                        id="input-market",
                        options=[
                            {"label": "OKC", "value": "OKC"},
                            {"label": "Dallas", "value": "Dallas"}
                        ],
                    )
                ]),
                dbc.Col([
                    html.P("Refresh Report", className='pt-3'),
                    dbc.Button("Refresh", id="update-fig", className="me-2", n_clicks=0),
                ]),
                dbc.Col([
                    html.Div(id='Generate-output')
                ])
            ]),
        ], width=6),
    ]),
    html.Div([
        dbc.Row([
            dcc.Loading(
                id="loading-Protocol_FIG",
                type="default",
                children=dcc.Graph(
                    id='Protocol_FIG',
                    figure={}
                )
            ),
        ], className="g-0"),
        dbc.Row([
            dcc.Loading(
                id="loading-DATA_FIG",
                type="default",
                children=dcc.Graph(
                    id='DATA_FIG',
                    figure={}
                )
            ),
        ], className="g-0"),
        dbc.Row([
            dcc.Loading(
                id="loading-VoNR_TECH_BAR_FIG",
                type="default",
                children=dcc.Graph(
                    id='VoNR_TECH_BAR_FIG',
                    figure={}
                )
            ),
        ], className="g-0"),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-VoNR_Result_MAP_FIG",
                    type="default",
                    children=dcc.Graph(
                        id='VoNR_Result_MAP_FIG',
                        figure={}
                    )
                ),
            ], width=6),
            dbc.Col([
                dcc.Loading(
                    id="loading-TECH_MAP_FIG",
                    type="default",
                    children=dcc.Graph(
                        id='TECH_MAP_FIG',
                        figure={}
                    )
                ),
            ], width=6),
        ], className="g-0"),
        dbc.Row([
            dcc.Loading(
                id="loading-Voice_HO_SINR_RSRP_BAR_FIG",
                type="default",
                children=dcc.Graph(
                    id='Voice_HO_SINR_RSRP_BAR_FIG',
                    figure={}
                )
            ),
        ], className="g-0"),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-RSRP",
                    type="default",
                    children=dcc.Graph(
                        id='RSRP_MAP_FIG',
                        figure={}
                    )
                ),
            ], width=6),
            dbc.Col([
                dcc.Loading(
                    id="loading-SINR",
                    type="default",
                    children=dcc.Graph(
                        id='SINR_MAP_FIG',
                        figure={}
                    )
                ),
            ], width=6)
        ], className="g-0"),
    ], className='rounded-lg')
], fluid=True)

app.layout = html.Div([
    navbar,
    dbc.Container([
        html.Div(id='page-content', children=[]),
    ], fluid=True)
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Upload':
        return Upload.layout
    else:
        return fig_layout


TEMP_NAME = []


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df = df.fillna(np.nan).replace([np.nan], ['NaN'])
            df['TIME_STAMP'] = df['TIME_STAMP'].astype(str)
            if TEMP_NAME != []:
                sh.del_worksheet(sh.worksheet(TEMP_NAME[0]))
                TEMP_NAME.clear()
            TEMP_NAME.append("TEMP_" + str(random.randint(0, 500)))
            try:
                Temp_worksheet = sh.add_worksheet(title=str(TEMP_NAME[0]), rows=100, cols=20)
            except:
                Temp_worksheet = sh.worksheet(str(TEMP_NAME[0]))
            Temp_worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.Hr(),  # horizontal line
    ])


@app.callback(Output('Protocol_FIG', 'figure'),
              Output('DATA_FIG', 'figure'),
              Output('VoNR_TECH_BAR_FIG', 'figure'),
              Output('VoNR_Result_MAP_FIG', 'figure'),
              Output('TECH_MAP_FIG', 'figure'),
              Output('Voice_HO_SINR_RSRP_BAR_FIG', 'figure'),
              Output('RSRP_MAP_FIG', 'figure'),
              Output('SINR_MAP_FIG', 'figure'),
              Input('my-date-picker-single-report', 'date'),
              Input('input-market', 'value'),
              Input('update-fig', 'n_clicks'),
              )
def update_output(date, market, n_clicks):
    if n_clicks is not None and market is not None:
        # Read Main DF DATA
        data_dataframe = pd.DataFrame(sh.worksheet("Data_" + date).get_all_records())
        data_dataframe = data_dataframe.convert_dtypes()
        data_dataframe = data_dataframe[data_dataframe['Date'] == date]
        data_market_DF = data_dataframe[data_dataframe['Market'] == market]
        # Read Main DF Voice
        voice_dataframe = pd.DataFrame(sh.worksheet("Voice_" + date).get_all_records())
        voice_dataframe = voice_dataframe.convert_dtypes()
        voice_dataframe = voice_dataframe[voice_dataframe['Date'] == date]
        voice_market_DF = voice_dataframe[voice_dataframe['Market'] == market]

        name = str(date) + " " + str(market)
        return Protocol_FIG(data_market_DF, name), \
               DATA_FIG(data_market_DF, name), \
               VoNR_TECH_BAR_FIG(voice_market_DF, name), \
               VoNR_Result_MAP_FIG(voice_market_DF, name), \
               TECH_MAP_FIG(voice_market_DF, name), \
               Voice_HO_SINR_RSRP_BAR_FIG(voice_market_DF, name), \
               RSRP_MAP_FIG(voice_market_DF, name), \
               SINR_MAP_FIG(voice_market_DF, name)
    else:
        raise dash.exceptions.PreventUpdate


@app.callback(Output('output-data-message', 'children'),
              Input('submit-val', 'n_clicks'),
              Input('input-market-upload', 'value')
              )
def update_output(n_clicks, market):
    if n_clicks > 0:
        T_dataframe = pd.DataFrame(sh.worksheet(TEMP_NAME[0]).get_all_records())
        T_ARRAY = []
        df_date = T_dataframe['TIME_STAMP'].iloc[0]
        date_string = str(df_date).split()[0]
        T_dataframe['Market'] = market
        T_dataframe['TIME_STAMP'] = T_dataframe['TIME_STAMP'].astype(str)
        for col in T_dataframe.columns:
            T_ARRAY.append(col)
        if T_ARRAY == Data_KPI_REQ:
            type = 'Data'
            try:
                Main_Data_worksheet = sh.add_worksheet(title=type + "_" + date_string, rows=100, cols=20)
            except:
                Main_Data_worksheet = sh.worksheet(type + "_" + date_string)
            M_dataframe = pd.DataFrame(Main_Data_worksheet.get_all_records())
            dataframe = pd.concat([M_dataframe, T_dataframe], axis=0)
            dataframe = dataframe.fillna(np.nan).replace([np.nan], ['NaN'])
            # Write Main DF
            Main_Data_worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
            sh.del_worksheet(sh.worksheet(TEMP_NAME[0]))
            TEMP_NAME.clear()
            return html.H5("TPUT Data uploaded successfully!", className='text-success')
        elif T_ARRAY == Voice_KPI_REQ:
            type = 'Voice'
            try:
                Main_Voice_worksheet = sh.add_worksheet(title=type + "_" + date_string, rows=100, cols=20)
            except:
                Main_Voice_worksheet = sh.worksheet(type + "_" + date_string)
            M_dataframe = pd.DataFrame(Main_Voice_worksheet.get_all_records())
            dataframe = pd.concat([M_dataframe, T_dataframe], axis=0)
            dataframe = dataframe.fillna(np.nan).replace([np.nan], ['NaN'])
            # Write Main DF
            Main_Voice_worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
            sh.del_worksheet(sh.worksheet(TEMP_NAME[0]))
            TEMP_NAME.clear()
            return html.H5("Voice Data uploaded successfully!", className='text-success')
        else:
            return html.Div([
                html.H5('ERROR: Either DATA TYPE is incorrect or you are missing KPIs!', className='text-danger'),
                html.H6('Provided KPI'),
                html.P(str(T_ARRAY)),
                html.Hr(),
                html.H6('Required KPI'),
                html.P(str(Data_KPI_REQ))
            ])
    return False
# html.Li(i) for i in worksheet_list

@app.callback(Output('output-data-upload', 'children'),
              Output('output-data-upload-settings', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children, html.Div([
            dbc.Row([
                dbc.Col([
                    html.P("Select Market", className='pt-3'),
                    dbc.Select(
                        id="input-market-upload",
                        options=[
                            {"label": "OKC", "value": "OKC"},
                            {"label": "Dallas", "value": "Dallas"}
                        ],
                    )
                ]),
                dbc.Col([
                    html.P("Upload Now", className='pt-3'),
                    dbc.Button(
                        "Upload", id="submit-val", className="me-2", n_clicks=0
                    ),
                ]),
            ])
        ])
    else:
        return False, False


if __name__ == '__main__':
    app.run_server(debug=False)
