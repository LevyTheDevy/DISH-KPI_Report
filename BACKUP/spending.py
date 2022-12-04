import pandas as pd
import plotly.express as px

df = pd.read_csv("activity.csv")

fig = px.bar(df, x='Date', y='Amount')

fig.show()