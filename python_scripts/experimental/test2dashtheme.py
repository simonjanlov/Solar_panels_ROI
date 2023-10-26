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
data = pd.read_csv('C://final_project//el_priser_data//testData_month_orig.csv')
df = pd.DataFrame(data)

bar_df = df.iloc[0, [5, 6, 7, 8, 9, 10, 11, 12]]
n_df = pd.DataFrame(bar_df)
n_df.reset_index(inplace=True)
n_df.rename(
    columns={"index": "Hours", 0: "No of Calls"},
    inplace=True
)
# Custom colors for the bar chart
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# Load the price prognoses data
price_prognoses_data = pd.read_csv('C://final_project//el_priser_data//predicted_prices.csv')

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
    options=['Package 1', 'Package 2', 'Package 3', 'Package 4'],
    value='Package 1',
    className='mb-3'  # Apply Bootstrap classes
)

# Wrap the second graph and both Dropdowns in a dcc.Loading container
second_graph = dcc.Loading(
    [
        dcc.Graph(figure=fig),
        city_dropdown,
        package_dropdown,
        html.Div(id='output')  # Output element to display selected city
    ]
)

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

# These buttons are added to the app just to show the Bootstrap theme colors
buttons = html.Div(
    [
        dbc.Button("Primary", color="primary"),
        dbc.Button("Secondary", color="secondary"),
        dbc.Button("Success", color="success"),
        dbc.Button("Warning", color="warning"),
        dbc.Button("Danger", color="danger"),
        dbc.Button("Info", color="info"),
        dbc.Button("Light", color="light"),
        dbc.Button("Dark", color="dark"),
        dbc.Button("Link", color="link"),
    ],
)

heading = html.H1("Dash Bootstrap Template Demo", className="bg-primary text-white p-2")

app.layout = dbc.Container(fluid=True, children=[heading, buttons, graphs])

@app.callback(
    Output('output', 'children'),
    [Input('city-dropdown', 'value')]
)
def update_output(selected_city):
    return f'Du har valt staden: {selected_city}'

if __name__ == "__main__":
    app.run_server(debug=True)
