import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

FIG_ARRAY = []

DATA_KPI = ["5G KPI PCell RF Serving SS-RSRP [dBm]",
            "5G KPI PCell RF Serving SS-SINR [dB]",
            "5G KPI Total Info Layer1 PDSCH Throughput [Mbps]",
            "5G KPI Total Info Layer1 PUSCH Throughput [Mbps]",
            "5G KPI PCell Layer1 DL MCS (Avg)",
            "5G KPI PCell Layer1 UL MCS (Avg)",
            "5G KPI PCell Layer1 DL BLER [%]",
            "5G KPI PCell Layer1 UL BLER [%]"]


def AVG_MIN_MAX(df, KPI):
    AVG = df[KPI].dropna().mean().round(2)
    MIN = df[KPI].dropna().min().round(4)
    MAX = df[KPI].dropna().max().round(2)
    return [AVG, MIN, MAX]


def DATA_FIG(df, name):
    df["AutoCallSummary Status"] = df["AutoCallSummary Status"].interpolate(method="pad")
    df_data = df[df["AutoCallSummary Status"] == "Traffic"]

    # Make Data Fig Subplots
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=DATA_KPI
    )
    COL = 0
    ROW = 1
    for k in DATA_KPI:
        if COL < 2:
            COL += 1
        else:
            ROW += 1
            COL = 1
        fig.add_trace(
            go.Bar(x=["AVG", "MIN", "MAX"], y=AVG_MIN_MAX(df_data, k),
                   text=AVG_MIN_MAX(df_data, k), name=k),
            row=ROW, col=COL
        )

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={
            'text': "<b> " + str(
                name) + " - Data KPI<b>"},
        )
    FIG_ARRAY.append(fig)
    return fig


def Protocol_FIG(df, name):
    s = df["5G KPI PCell Layer1 RACH Result"].value_counts()
    df_rach_count = s.to_frame(name='Count')

    s = df["5G KPI Total Info DL CA Type"].value_counts()
    df_ca_count = s.to_frame(name='Count')

    s = df["5G KPI PCell Layer1 RACH Reason"].value_counts()
    df_RACH_Reason_count = s.to_frame(name='Count')

    s = df["5G KPI PCell RF Band"].value_counts()
    df_BAND_count = s.to_frame(name='Count')

    # Make Protocol Fig Subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]],
        subplot_titles=(
            "5G KPI PCell Layer1 RACH Result", "5G KPI Total Info DL CA Type", "5G KPI PCell Layer1 RACH Reason",
            "5G KPI PCell RF Band")
    )

    df_rach_count['Percentage'] = round((df_rach_count['Count'] / df_rach_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_rach_count['Count'], x=df_rach_count.index, legendgroup="RACH Results",
               legendgrouptitle_text="<b>5G KPI PCell Layer1 RACH Result<b>",
               name="RACH Results",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                     zip(df_rach_count['Count'], df_rach_count['Percentage'])]
               ),

        row=1, col=1
    )

    df_ca_count['Percentage'] = round((df_ca_count['Count'] / df_ca_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_ca_count['Count'], x=df_ca_count.index, legendgroup="CA",
               legendgrouptitle_text="<b>5G KPI Total Info DL CA Type<b>",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in zip(df_ca_count['Count'], df_ca_count['Percentage'])]
               ),
        row=1, col=2
    )

    df_RACH_Reason_count['Percentage'] = round(
        (df_RACH_Reason_count['Count'] / df_RACH_Reason_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_RACH_Reason_count['Count'], x=df_RACH_Reason_count.index, legendgroup="RACH",
               legendgrouptitle_text="<b>5G KPI PCell Layer1 RACH Reason<b>",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                     zip(df_RACH_Reason_count['Count'], df_RACH_Reason_count['Percentage'])],
               name="RACH Reason"),
        row=2, col=1
    )

    df_BAND_count['Percentage'] = round((df_BAND_count['Count'] / df_BAND_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_BAND_count['Count'], x=df_BAND_count.index, legendgroup="BAND",
               legendgrouptitle_text="<b>5G KPI PCell RF Band<b>", text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                                                                         zip(df_BAND_count['Count'],
                                                                             df_BAND_count['Percentage'])],
               name="5G KPI PCell RF Band"),
        row=2, col=2
    )

    fig.update_traces(textfont_size=15, textangle=0, cliponaxis=False)

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={
            'text': "<b>" + str(name) + " - Protocol KPI<b>"},
        )
    FIG_ARRAY.append(fig)
    return fig


px.set_mapbox_access_token(open("assets/map.mapbox_token").read())


def RSRP_MAP_FIG(df, name):
    df = df[df["5G KPI PCell RF Serving SS-RSRP [dBm]"].notna()]
    # Make Voice Fig Subplots
    RSRP_fig = px.scatter_mapbox(df, lat="GPS Lat", lon="GPS Lon", color="5G KPI PCell RF Serving SS-RSRP [dBm]",
                                 color_continuous_scale=[(0, "red"), (0.5, "yellow"), (1, "green")], size_max=20,
                                 zoom=10.5,
                                 labels={"5G KPI PCell RF Serving SS-RSRP [dBm]": "<b>RSRP [dBm]<b>"})

    RSRP_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - RSRP - MAP<b>"},
                           )
    FIG_ARRAY.append(RSRP_fig)
    return RSRP_fig


def SINR_MAP_FIG(df, name):
    df = df[df["5G KPI PCell RF Serving SS-SINR [dB]"].notna()]
    SINR_fig = px.scatter_mapbox(df, lat="GPS Lat", lon="GPS Lon", color="5G KPI PCell RF Serving SS-SINR [dB]",
                                 color_continuous_scale=[(0, "red"), (0.5, "yellow"), (1, "green")], size_max=20,
                                 zoom=10.5,
                                 labels={"5G KPI PCell RF Serving SS-SINR [dB]": "<b>SINR [dB]<b>"})

    SINR_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - SINR - MAP<b>"},
                           )
    FIG_ARRAY.append(SINR_fig)
    return SINR_fig


def VoNR_Result_MAP_FIG(df, name):
    df = df.replace(to_replace="End By Pause", value="No Page")
    df = df.replace(to_replace="End By User", value="Success")
    df["GPS Lon"] = df["GPS Lon"].fillna(method='ffill')
    df["GPS Lat"] = df["GPS Lat"].fillna(method='ffill')

    map_df = df[df['Voice Call'].notna()]

    results_fig = px.scatter_mapbox(map_df, lat="GPS Lat", lon="GPS Lon", color="Voice Call", size_max=20, zoom=10.5,
                                    labels={"Voice Call": "<b>VoNR Results<b>"})

    results_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - Voice Call - MAP<b>"},
                              )
    FIG_ARRAY.append(results_fig)
    return results_fig


def TECH_MAP_FIG(df, name):
    df = df.replace(to_replace="5G-NR_SA(2CA)", value="5G-NR_SA")
    df = df.replace(to_replace="LTE(2CA)", value="LTE")
    map_df = df[df['Event Technology'].notna()]

    tech_results_fig = px.scatter_mapbox(map_df, lat="GPS Lat", lon="GPS Lon", color="Event Technology", size_max=20,
                                         zoom=10.5,
                                         labels={"Event Technology": "<b>Event Technology<b>"})

    tech_results_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - Event Technology - MAP<b>"},
                                   )
    FIG_ARRAY.append(tech_results_fig)
    return tech_results_fig


def VoNR_TECH_BAR_FIG(df, name):
    df = df.replace(to_replace="5G-NR_SA(2CA)", value="5G-NR_SA")
    df = df.replace(to_replace="LTE(2CA)", value="LTE")
    df = df.replace(to_replace="End By Pause", value="No Page")
    df = df.replace(to_replace="End By User", value="Success")

    # Getting the string count of call result to int
    s = df["Voice Call"].value_counts()
    # Make a DF from call results
    df_voice_count = s.to_frame(name='Count')

    # Getting the string count of call result to int
    s = df["Event Technology"].value_counts()
    # Make a DF from call results
    df_tech_count = s.to_frame(name='Count')

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}]],
        subplot_titles=("<b>Voice Call<b> <br>  <br>",
                        "<b>Event Technology<b> <br>  <br>",
                        )
    )

    fig.add_trace(
        go.Pie(values=df_voice_count['Count'], labels=df_voice_count.index, legendgroup="CALL",
               legendgrouptitle_text="<b>Voice Call<b>", name="Call Results"),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(values=df_tech_count['Count'], labels=df_tech_count.index, legendgroup="TECH",
               legendgrouptitle_text="<b>Event Technology<b>", name="Technology"),
        row=1, col=2
    )

    fig.update_traces(textposition='auto', textinfo='value+percent+label')

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={
            'text': "<b>" + str(
                name) + " - Voice KPI<b>"},
        
    )
    FIG_ARRAY.append(fig)
    return fig


def Voice_HO_SINR_RSRP_BAR_FIG(df, name):
    # Getting the string count of call result to int
    s = df["5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverResult"].value_counts()
    # Make a DF from call results
    df_HO_count = s.to_frame(name='Count')

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]],
        subplot_titles=("RSRP",
                        "5G-NR HO Results",
                        "SINR"
                        )
    )

    df_HO_count['Percentage'] = round((df_HO_count['Count'] / df_HO_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_HO_count['Count'], x=df_HO_count.index, legendgroup="HO",
               legendgrouptitle_text="<b>5G-NR Handover Result<b>", name="5G-NR Handover Result",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                     zip(df_HO_count['Count'], df_HO_count['Percentage'])], ),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MAX", "MIN"], y=[df["5G KPI PCell RF Serving SS-RSRP [dBm]"].mean().round(2),
                                           df["5G KPI PCell RF Serving SS-RSRP [dBm]"].min().round(4),
                                           df["5G KPI PCell RF Serving SS-RSRP [dBm]"].max().round(2)],
               legendgroup="Voice RF", legendgrouptitle_text="<b>Voice RF<b>",
               text=[df["5G KPI PCell RF Serving SS-RSRP [dBm]"].mean().round(2),
                     df["5G KPI PCell RF Serving SS-RSRP [dBm]"].min().round(4),
                     df["5G KPI PCell RF Serving SS-RSRP [dBm]"].max().round(2)], name="RSRP"),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df["5G KPI PCell RF Serving SS-SINR [dB]"].mean().round(2),
                                           df["5G KPI PCell RF Serving SS-SINR [dB]"].min().round(4),
                                           df["5G KPI PCell RF Serving SS-SINR [dB]"].max().round(2)],
               legendgroup="Voice RF", text=[df["5G KPI PCell RF Serving SS-SINR [dB]"].mean().round(2),
                                             df["5G KPI PCell RF Serving SS-SINR [dB]"].min().round(4),
                                             df["5G KPI PCell RF Serving SS-SINR [dB]"].max().round(2)],
               name="SINR"),
        row=1, col=3
    )

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={
            'text': "<b>" + str(
                name) + " - Voice KPI<b>"},
        )
    FIG_ARRAY.append(fig)
    return fig
