import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

# Import and clean data (importing CSV into pandas)
df = pd.read_csv('C:/Users/User/Desktop/python final/MODIS_C6_1_Global_24h.csv')
df['text'] = df['acq_date'].astype(str) + ',' + df['acq_time'].astype(str) + ',' + df['daynight'].astype(str) + ',' + df['brightness'].astype(str) + ',' + df['scan'].astype(str)

print(df)

# App layout
app.layout = html.Div([
    html.H1('世界大火地圖', style={'text-align': 'center'}),
    dcc.Dropdown(id='slct_date',
                 options=[
                     {'label': '2023/6/9', 'value': '2023/6/9'}
                 ],
                 multi=False,
                 value='2023/6/9',
                 style={'width': '40%'}
                 ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_fire_map', figure={})
])

# Connect the plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_fire_map', component_property='figure')],
    [Input(component_id='slct_date', component_property='value')]
)
def update_graph(options_slctd):
    print(options_slctd)
    print(type(options_slctd))

    container = "The date was: {}".format(options_slctd)

    filtered_df = df[df["acq_date"] == options_slctd]

    # Plotly Express
    fig = go.Figure(
        data=go.Scattergeo(
            lon=filtered_df['longitude'],
            lat=filtered_df['latitude'],
            text=filtered_df['text'],
            mode='markers',
            marker_color=filtered_df['brightness'],
            marker=dict(
                size=filtered_df['scan'].astype(float) * 5,
                opacity=0.8,
                reversescale=True,
                autocolorscale=False,
                symbol='circle',
                line=dict(
                    width=1,
                    color='rgba(255,255,255)'
                ),
                colorscale='Oranges',
                cmin=290,
                color=filtered_df['brightness'],
                cmax=370,
                colorbar_title="2023/6/9 Brightness"
            )
        )
    )
    fig.update_layout(
        title='World Fire Map - 24hr',
    )
    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)


