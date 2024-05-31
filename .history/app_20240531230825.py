from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import csv
import os

csv_file_path = os.path.join(os.path.dirname(__file__), "sales.csv")

# Error handler to confirm that the locally imported csv file exists. Officially, you would need an API supplying that data
if os.path.exists(csv_file_path):
    # Open and read the CSV file
    with open(csv_file_path, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
else:
    print("stop.csv file not found.")


df = pd.read_csv(csv_file_path)

bootstrap = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=bootstrap)

## Add application style layout - this concerns the general UI of the dashboard
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1(
                    "Analysing Sales, Markup, and Contribution Margin",
                    className="text-success text-center fs-3 fw-bolder",
                )
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label(
                            children="Select metric",
                            html_for="filter-options",
                            className="fw-bolder text-success mt-4",
                        ),
                        dbc.Select(
                            options=[
                                {"label": x, "value": x}
                                for x in [
                                    "cost",
                                    "markup",
                                    "revenue",
                                    "contributionMargin",
                                    "contributionMarginPct",
                                ]
                            ],
                            value="revenue",
                            id="filter-options",
                            className="form-select mb-4 w-25 mx-2",
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.H2(children="Table", className="h5 text-success"),
                        dbc.Col(
                            [
                                dash_table.DataTable(
                                    data=df.to_dict("records"),
                                    page_size=6,
                                    style_table={"overflowX": "auto"},
                                )
                            ],
                            width=12,
                        ),
                        dbc.Col(
                            [dcc.Graph(figure={}, id="contribution-margin-graph")],
                            width=12,
                        ),
                    ]
                ),
            ],
            className="d-flex flex-lg-column row vstack gap-3",
        ),
    ],
    fluid=True,
)


## Callback needed to add interactive effects - For every filter function selected from the dropdown, output should
## reflect that upon the graph
@callback(
    Output(component_id="contribution-margin-graph", component_property="figure"),
    Input(component_id="filter-options", component_property="value"),
)
def update_graph(selected_column):
    fig = px.histogram(df, x="product", y=selected_column, histfunc="avg")
    return fig


if __name__ == "__main__":
    app.run(
        debug=True
    )  ## This helps the developer catch bugs - perhaps due to improperly mapped fields
