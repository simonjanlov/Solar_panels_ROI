from dash import Dash, dcc, html, Input, Output,callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# Load the "vapor" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io, and makes it the default figure template.
load_figure_template("vapor")

# Create a Dash app with Bootstrap "vapor" theme
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

# Load your existing data
data = pd.read_csv('C:\\Users\\henry\\Documents\\projekt\\Visualization\\CustomerService\\data\\testData_month_orig.csv')
df = pd.DataFrame(data)

bar_df = df.iloc[0, [5, 6, 7, 8, 9, 10, 11, 12]]
n_df = pd.DataFrame(bar_df)
n_df.reset_index(inplace=True)
n_df.rename(
    columns={"index": "Hours", 0: "No of Calls"},
    inplace=True
)
# Custom colors for the bar chart
bar_colors = ['#1f77b4', 'black', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# Load the price prognoses data
price_prognoses_data = pd.read_csv('C:\\Users\\henry\\Documents\\projekt\\examens_proj\\final_project\\data\\predicted_prices.csv')

prognoses_fig = px.line(price_prognoses_data, x='Year', y='Predicted kWh price', title='Price Prognoses')

fig = px.bar(n_df, x='Hours', y='No of Calls', title='Return of Investment', color='Hours',
             color_discrete_sequence=bar_colors)

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
    options=['0°', '10°', '20°', '30°', '40°', '50°', '60°', '70°', '80°', '90°'],
    value='20°',
    className='mb-3'  # Apply Bootstrap classes
)
direction_dropdown = dcc.Dropdown(
    id='direction-dropdown',
    options=['West', 'South West', 'South', 'South East', 'East'],
    value='South West',
    className='mb-3'  # Apply Bootstrap classes
)



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
            dcc.Graph(figure=fig),
            
            html.Div(id='output')  # Output element to display selected city
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
app.layout = dbc.Container(fluid=True, children=[heading, graphs])

@app.callback(
    Output('output', 'children'),
    [Input('city-dropdown', 'value'),
     Input('package-dropdown', 'value'),
     Input('angle-dropdown', 'value'),
     Input('direction-dropdown', 'value')]
)
def update_output(selected_city,selected_package,selected_angle,selected_direction):
    return f"You have chosen: {selected_city}, {selected_package}, {selected_angle}, {selected_direction}"


if __name__ == "__main__":
    app.run_server(debug=True)
