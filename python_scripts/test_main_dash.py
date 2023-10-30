from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# Import class and functions
from electricity_output_calc import SolarPanelSystem
from find_tilt_and_direction_value import find_tilt_and_direction_value
from calc_years_until_breakeven import calc_years_until_breakeven

# Import the data for cities and solar packages
from data_dicts import packages_dict, cities_dict, years_list


# Load the "superhero" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io, and makes it the default figure template.
load_figure_template("superhero")

# Create a Dash app with Bootstrap "superhero" theme
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

# Load the price prognoses data
price_prognoses_data = pd.read_csv(r'data\predicted_prices_withzones.csv')
data = pd.read_csv(r'data\Electricity generation by source - Sweden.csv')
df = pd.DataFrame(data)
df.drop(columns=['Unnamed: 0'], inplace=True)
sums = df.sum()
fig1 = px.pie(names=sums.index, values=sums.values, title='Energy source destribution in Sweden')
fig1.update_traces(pull=[0,0,0,0,0,0,0,0,0.2])


# Create the line graph for the price predictions
prognoses_fig = px.line(price_prognoses_data, 
                        x='Year', 
                        y=['Predicted kWh price', 'zone1', 'zone2', 'zone3', 'zone4'], 
                        title='Price Forecast (per electricity zone)')
prognoses_fig.update_traces(name="zone 1", selector=dict(name="zone1"))
prognoses_fig.update_traces(name="zone 2", selector=dict(name="zone2"))
prognoses_fig.update_traces(name="zone 3", selector=dict(name="zone3"))
prognoses_fig.update_traces(name="zone 4", selector=dict(name="zone4"))
prognoses_fig.update_layout(legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"), 
                            yaxis_title="predicted price (SEK/kWh)", 
                            xaxis_title="",plot_bgcolor="#11293D")

# Create the gauge figure
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=15,
    domain={'x': [0, 1], 'y': [0, 1],
            'row': 0, 'column': 0},
    title={'text': "No of years "},
    gauge={'bar': {'color': "#f98435"}  # Change the color here
    }))

# Create the graph for the profitability
tilt_and_direction = find_tilt_and_direction_value(20, '225 SV')
my_system = SolarPanelSystem(system_cost=packages_dict['12 solar panels']['system_cost'],
                             system_effect_kWp=packages_dict['12 solar panels']['system_effect'],
                             insolation=cities_dict['Luleå']['insolation'],
                             tilt_and_direction=tilt_and_direction)
profit_values = my_system.profitability_over_time(cities_dict['Luleå']['predicted_prices'])
years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})

# round the values for hover output purposes (round -3 means even thousands, round -2 will give one "decimal")
years_profit_df['Profit'] = [round(x, -2) if abs(x) > 1000 else x for x in profit_values]

main_fig = px.bar(years_profit_df, x='Years', y='Profit', title='Return of Investment', hover_data={'Profit':':.2f'})
main_fig.update_layout(plot_bgcolor="#11293D")

# Create Dropdowns for the second graph
city_dropdown = dcc.Dropdown(
    id='city-dropdown',
    options=['Malmö', 'Stockholm', 'Sundsvall', 'Luleå'],
    value='Malmö',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)

package_dropdown = dcc.Dropdown(
    id='package-dropdown',
    options=['12 solar panels', '25 solar panels', '35 solar panels', '45 solar panels'],
    value='25 solar panels',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)

angle_dropdown = dcc.Dropdown(
    id='angle-dropdown',
    options=['0°', '10°', '20°', '30°', '40°', '50°', '60°', '70°', '80°', '90°'],
    value='40°',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)
direction_dropdown = dcc.Dropdown(
    id='direction-dropdown',
    options=['West', 'South West', 'South', 'South East', 'East'],
    value='West',
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
        html.Label("Select Tilt"),
        angle_dropdown,
    ], width=3),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Direction"),
        direction_dropdown,
    ], width=3),  # Adjust the width as needed
], className="mb-3")


# Create a callback for updating the chart
@app.callback(
    [Output('line-chart', 'figure'),
     Output('circle-with-number', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('package-dropdown', 'value'),
     Input('angle-dropdown', 'value'),
     Input('direction-dropdown', 'value')]
)
def update_output(selected_city, selected_package, selected_angle, selected_direction):
    
    # replace user friendly value with the real csv file name (of direction)
    direction_dropdown_values = ['West', 'South West', 'South', 'South East', 'East']
    direction_csv_columns = ['270 V', '225 SV', '180 S', '135 SO', '90 E']
    for i in range(len(direction_dropdown_values)):
        if selected_direction == direction_dropdown_values[i]:
            selected_direction = direction_csv_columns[i]
            break


    # update the bar chart
    selected_angle = selected_angle[:selected_angle.find('°')]
    tilt_and_direction = find_tilt_and_direction_value(int(selected_angle), selected_direction)
    
    my_system = SolarPanelSystem(system_cost=packages_dict[selected_package]['system_cost'],
                                 system_effect_kWp=packages_dict[selected_package]['system_effect'],
                                 insolation=cities_dict[selected_city]['insolation'],
                                 tilt_and_direction=tilt_and_direction)
    
    profit_values = my_system.profitability_over_time(cities_dict[selected_city]['predicted_prices'])
    years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})
    
    # round the values for hover output purposes (round -3 means even thousands, round -2 will give one "decimal")
    years_profit_df['Profit'] = [round(x, -2) if abs(x) > 1000 else x for x in profit_values]

    main_fig = px.bar(years_profit_df, x='Years', y='Profit', title='Return of Investment')
    main_fig.update_layout(yaxis_title="Profitability (SEK)", xaxis_title="",plot_bgcolor="#11293D")

    # update the numerical figure
    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=calc_years_until_breakeven(years_list, profit_values),
    domain={'x': [0, 1], 'y': [0, 1],
            'row': 0, 'column': 0},
    title={'text': "Years until breakeven"},
    gauge={'bar': {'color': "#f98435"},
            'axis': {'range': [0, 30]}  # Change the color here
    }))
    
    return main_fig, fig


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
                                html.H2('Solar Panels: Return on Invested Capital', style={'font-size': '34px', 'font-weight': 'bold', 'text-align': 'center', 'margin-bottom': '20px'}),
                                dropdown_row,
                                
                            ],
                                width=8,
                                className="mb-3",
                                style={"margin-top": "40px"}
                            ),
                            # Add justify-content-center to center the content
                            className="justify-content-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id='line-chart', figure=main_fig), lg=6),
                                dbc.Col(dcc.Graph(id='circle-with-number', figure=fig), lg=6),
                                
                            ],
                            className="mt-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(figure=fig1), lg=6),
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
