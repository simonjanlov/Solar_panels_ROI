from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash.dependencies import Input, Output



data = pd.read_csv('C:\\Users\\henry\\Documents\\projekt\\Visualization\\CustomerService\\data\\testData_month_orig.csv')
df = pd.DataFrame(data)

bar_df = df.iloc[0, [5, 6, 7, 8, 9, 10, 11, 12]]
n_df = pd.DataFrame(bar_df)
n_df.reset_index(inplace=True)
n_df.rename(
    columns={"index": "Hours", 0: "No of Calls"},
    inplace=True
)




app = Dash(__name__)

fig = px.bar(n_df, x='Hours', y='No of Calls', title='Return of Investment',color='Hours')
# fig_map = px.choropleth_mapbox(
#     geojson=px.data.gapminder().query("country == 'Sweden'"),
#     locations="country",
#     color="country",
#     featureidkey="properties.name",
#     mapbox_style="carto-positron",
# )




app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Välj en stad i din elzon'),
            dcc.Dropdown(
                id='city-dropdown',
                options=['Malmö', 'Stockholm', 'Sundsvall', 'Luleå'],
                value='Luleå',
                style={'width': '200px', 'font-size': '18px', 'margin-right': '20px'}
            ),
            html.Div(id='output')
        ]),
        html.Div([
            html.Label('Välj det paket som passa ditt tak'),
            dcc.Dropdown(
                options=['Package 1', 'Package 2', 'Package 3', 'Package 4'],
                value='Package 1',
                style={'width': '200px', 'font-size': '18px', 'margin-right': '20px'}
            )
        ]),
        html.Div([
            html.Label('Välj en vinkel på ditt tak'),
            dcc.Dropdown(
                options=['0', '10', '20', '30', '40', '50', '60', '70', '80', '90'],
                value='20',
                style={'width': '200px', 'font-size': '18px', 'margin-right': '20px'}
            )
        ]),
        html.Div([
            html.Label('Mot vilket väderstreck vetter ditt tak?'),
            dcc.Dropdown(
                options=['West', 'South West', 'South', 'South East', 'East'],
                value='West',
                style={'width': '200px', 'font-size': '18px', 'margin-right': '20px'}
            ),
        ])
    ], style={'display': 'flex'}),
    html.Div([
        dcc.Graph(
            id='line chart',
            figure=fig,
            style={'width': '1000px', 'height': '600px'}
        ),
        # dcc.Graph(figure=fig_map, style={'width': '50%', 'display': 'inline-block'})
    ],style={'display':'flex'})
])

        
@app.callback(
    Output('output', 'children'),
    [Input('city-dropdown', 'value')]
)
def update_output(selected_city):
    print(f'Du har valt staden: {selected_city}')
    return f'Du har valt staden: {selected_city}'







if __name__ == '__main__':
    app.run(debug=True)