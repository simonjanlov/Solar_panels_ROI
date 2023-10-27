from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# import class and function for Solar panel
from electricity_output_calc import SolarPanelSystem
from find_tilt_and_direction_value import find_tilt_and_direction_value

# import the data for cities and solar packages
from data_dicts import packages_dict, cities_dict, years_list


# Load the "vapor" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io, and makes it the default figure template.
load_figure_template("vapor")

# Create a Dash app with Bootstrap "vapor" theme
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])


# Load the price prognoses data
price_prognoses_data = pd.read_csv(r'data\predicted_prices.csv')

prognoses_fig = px.line(price_prognoses_data, x='Year', y='Predicted kWh price', title='Price Prognoses')

# Create Dropdowns for the second graph
city_dropdown = dcc.Dropdown(
    id='city-dropdown',
    options=['Malmö', 'Stockholm', 'Sundsvall', 'Luleå'],
    value='Luleå',
    className='mb-3'  # Apply Bootstrap classes
)

package_dropdown = dcc.Dropdown(
    id='package-dropdown',
    options=['Package 1 (12 solar panels)', 'Package 2 (25 solar panels)', 'Package 3 (35 solar panels)', 'Package 4 (45 solar panels)'],
    value='Package 1 (12 solar panels)',
    className='mb-3'  # Apply Bootstrap classes
)

angle_dropdown = dcc.Dropdown(
    id='angle-dropdown',
    options=['0', '10', '20', '30', '40', '50', '60', '70', '80', '90'],
    value='20',
    className='mb-3'  # Apply Bootstrap classes
)
direction_dropdown = dcc.Dropdown(
    id='direction-dropdown',
    options=['270 V', '225 SV', '180 S', '135 SO', '90 E'],
    value='225 SV',
    className='mb-3'  # Apply Bootstrap classes
)


tilt_and_direction = find_tilt_and_direction_value(20, '225 SV')
my_system = SolarPanelSystem(system_cost=packages_dict['Package 1 (12 solar panels)']['system_cost'],
                             system_effect_kWp=packages_dict['Package 1 (12 solar panels)']['system_effect'],
                             insolation=cities_dict['Luleå']['insolation'], 
                             tilt_and_direction=tilt_and_direction)
profit_values = my_system.profitability_over_time(cities_dict['Luleå']['predicted_prices'])

years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})
main_fig = px.bar(years_profit_df, x='Years', y='Profit', title='Return of Investment')



dropdown_frame = html.Div([    
    html.Label("Select City"),
    city_dropdown,
    html.Label("Select Package"),
    package_dropdown,    
    html.Label("Select Angle"),    
    angle_dropdown,    
    html.Label("Select Direction"),    
    direction_dropdown,
    ], className="dropdown-frame",style={'border': '3px solid black', 'padding': '10px'})# Apply Bootstrap classes)# Wrap the second graph and both Dropdowns in a dcc.Loading container

second_graph = dcc.Loading(
        [    
            dropdown_frame,    
            dcc.Graph(id='line-chart',figure=main_fig),
                    ])

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=prognoses_fig), lg=6),
                dbc.Col(second_graph, lg=6),
            ],
            className="mt-4",
        ),
    ]
)



heading = html.H1("Solar Panels: Return of Investment", className="bg-primary text-white p-2",style={"text-align": "center"})
app.layout = dbc.Container(fluid=True, children=[
    heading,
    graphs,
    
])



@app.callback(
    [Output('line-chart', 'figure')],  # Lägg till line chart som en output    
    [Input('city-dropdown', 'value'),
    Input('package-dropdown', 'value'),
    Input('angle-dropdown', 'value'),
    Input('direction-dropdown', 'value')]
)

def update_output(selected_city, selected_package, selected_angle, selected_direction):
    # test_df = pd.DataFrame({'x': [selected_city, selected_package], 'y': [len(selected_angle), len(selected_direction)]})
    # fig = px.bar(test_df, x='x', y='y', title='Return of Investment')
    # return fig,

        
    tilt_and_direction = find_tilt_and_direction_value(int(selected_angle), selected_direction)
    my_system = SolarPanelSystem(system_cost=packages_dict[selected_package]['system_cost'],
                                system_effect_kWp=packages_dict[selected_package]['system_effect'],
                                insolation=cities_dict[selected_city]['insolation'], 
                                tilt_and_direction=tilt_and_direction)
    profit_values = my_system.profitability_over_time(cities_dict[selected_city]['predicted_prices'])

    years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})
    main_fig = px.bar(years_profit_df, x='Years', y='Profit', title='Return of Investment')

    # calculate the big number (years until breakeven)
    

    return main_fig,
    


if __name__ == "__main__":
    app.run_server(debug=True)
