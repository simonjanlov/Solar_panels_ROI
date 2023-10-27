from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# Import class and function for Solar panel
from electricity_output_calc import SolarPanelSystem
from find_tilt_and_direction_value import find_tilt_and_direction_value

# Import the data for cities and solar packages
from data_dicts import packages_dict, cities_dict, years_list

# Load the "vapor" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io, and makes it the default figure template.
load_figure_template("vapor")

# Create a Dash app with Bootstrap "vapor" theme
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

# Load the price prognoses data
price_prognoses_data = pd.read_csv(r'el_priser_data\data\predicted_prices_withzones.csv')

prognoses_fig = px.line(price_prognoses_data, x='Year', y='Predicted kWh price', title='Price Prognoses')
prognoses_fig = px.line(price_prognoses_data, x='Year', y=['Predicted kWh price', 'zone1', 'zone2', 'zone3', 'zone4'], title='Price Prognoses')
prognoses_fig.update_layout(legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"))

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=15,
    domain={'x': [0, 1], 'y': [0, 1],
            'row': 0, 'column': 0},
    title={'text': "No of years "},
    gauge={'bar': {'color': "blue"}  # Change the color here
    }))

# Create Dropdowns for the second graph
city_dropdown = dcc.Dropdown(
    id='city-dropdown',
    options=['Malmö', 'Stockholm', 'Sundsvall', 'Luleå'],
    value='Luleå',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)

package_dropdown = dcc.Dropdown(
    id='package-dropdown',
    options=['Package 1 (12 solar panels)', 'Package 2 (25 solar panels)', 'Package 3 (35 solar panels)', 'Package 4 (45 solar panels)'],
    value='Package 1 (12 solar panels)',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)

angle_dropdown = dcc.Dropdown(
    id='angle-dropdown',
    options=['0', '10', '20', '30', '40', '50', '60', '70', '80', '90'],
    value='20',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)
direction_dropdown = dcc.Dropdown(
    id='direction-dropdown',
    options=['270 V', '225 SV', '180 S', '135 SO', '90 E'],
    value='225 SV',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)
dropdown_row = dbc.Row([
    dbc.Col([
        html.Label("Select City"),
        city_dropdown,
    ], width=3),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Package"),
        package_dropdown,
    ], width=3),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Angle"),
        angle_dropdown,
    ], width=3),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Direction"),
        direction_dropdown,
    ], width=3),  # Adjust the width as needed
], className="mb-3")

# centered_dropdown_div = html.Div(
#     dbc.Row(
#         dbc.Col(dropdown_row, width={"size": 6, "offset": 3}),
#         className="mb-3",
#     ),
#     style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "80vh"}
# )

tilt_and_direction = find_tilt_and_direction_value(20, '225 SV')
my_system = SolarPanelSystem(system_cost=packages_dict['Package 1 (12 solar panels)']['system_cost'],
                             system_effect_kWp=packages_dict['Package 1 (12 solar panels)']['system_effect'],
                             insolation=cities_dict['Luleå']['insolation'],
                             tilt_and_direction=tilt_and_direction)
profit_values = my_system.profitability_over_time(cities_dict['Luleå']['predicted_prices'])

years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})
main_fig = px.bar(years_profit_df, x='Years', y='Profit', title='Return of Investment')

# Create a callback for updating the chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('package-dropdown', 'value'),
     Input('angle-dropdown', 'value'),
     Input('direction-dropdown', 'value')]
)
def update_output(selected_city, selected_package, selected_angle, selected_direction):
    tilt_and_direction = find_tilt_and_direction_value(int(selected_angle), selected_direction)
    my_system = SolarPanelSystem(system_cost=packages_dict[selected_package]['system_cost'],
                                 system_effect_kWp=packages_dict[selected_package]['system_effect'],
                                 insolation=cities_dict[selected_city]['insolation'],
                                 tilt_and_direction=tilt_and_direction)
    profit_values = my_system.profitability_over_time(cities_dict[selected_city]['predicted_prices'])
    years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})
    main_fig = px.bar(years_profit_df, x='Years', y='Profit', title='Return of Investment')
    return main_fig

# Define the app layout
# ... (your existing code above)

# Define the app layout
app.layout = dbc.Container(fluid=True, children=[
    html.Div([
        # Add the gauge indicator here
        dbc.Row(
            [
                dbc.Col(dcc.Loading(
                    [
                        # Center the dropdown menu in the middle of the Dash app
                        dbc.Row(
                            dbc.Col([
                                html.H4('Choose Your Fighter', style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center'}),
                                dropdown_row,
                            ],
                                width=6,
                                className="mb-3",
                            ),
                            # Add justify-content-center to center the content
                            className="justify-content-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id='line-chart', figure=main_fig), lg=6),
                                dbc.Col(dcc.Graph(figure=fig), lg=6),
                                
                            ],
                            className="mt-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(figure=fig), lg=6),
                                dbc.Col(dcc.Graph(figure=prognoses_fig), lg=6)
                            ],
                            className="mt-4",
                        ),
                    ],
                )),
            ],
        ),
    ]),
])


if __name__ == "__main__":
    app.run_server(debug=True)
