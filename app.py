import os
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# ---- Data ----
df = px.data.gapminder().rename(columns={
    "country": "Country",
    "continent": "Continent",
    "year": "Year",
    "lifeExp": "Life Expectancy",
    "gdpPercap": "GDP per Capita",
    "pop": "Population",
})

# ---- App ----
app = Dash(__name__)
app.title = "Gapminder Analytics"

continents = sorted(df["Continent"].unique())
years = sorted(df["Year"].unique())

app.layout = html.Div([
    html.H1("Gapminder Analytics (Dash + Plotly)"),
    html.P("Explore life expectancy, GDP per capita, and population by country and year."),

    html.Div([
        html.Div([
            html.Label("Continent"),
            dcc.Dropdown(
                id="continent",
                options=[{"label": c, "value": c} for c in continents],
                value=continents[0],
                clearable=False
            ),
        ], style={"flex": "1", "minWidth": 200, "marginRight": 12}),

        html.Div([
            html.Label("Year"),
            dcc.Slider(
                id="year",
                min=min(years), max=max(years), step=5,
                marks={y: str(y) for y in years[::5]},
                value=years[0]
            ),
        ], style={"flex": "3", "minWidth": 260}),
    ], style={"display": "flex", "flexWrap": "wrap", "gap": 12}),

    dcc.Graph(id="scatter", style={"height": "520px", "marginTop": 16}),
    dcc.Graph(id="bar_pop", style={"height": "520px"}),
    dcc.Graph(id="bar_gdp", style={"height": "520px"}),

    html.Hr(),
    html.Div("Made with Dash & Plotly • Data: gapminder"),
], style={"maxWidth": 1100, "margin": "0 auto", "padding": "16px"})

# ---- Callbacks ----
@app.callback(
    Output("scatter", "figure"),
    [Input("continent", "value"), Input("year", "value")],
)
def update_scatter(continent, year):
    filtered = df[(df["Continent"] == continent) & (df["Year"] == year)]
    fig = px.scatter(
        filtered, x="GDP per Capita", y="Life Expectancy",
        size="Population", color="Country", hover_name="Country",
        size_max=45, title=f"{continent} — {year}: Life Expectancy vs GDP per Capita"
    )
    fig.update_layout(paper_bgcolor="#f5f7fb")
    return fig

@app.callback(
    Output("bar_pop", "figure"),
    [Input("continent", "value"), Input("year", "value")],
)
def update_bar_pop(continent, year):
    filtered = df[(df["Continent"] == continent) & (df["Year"] == year)]
    top = filtered.sort_values("Population", ascending=False).head(15)
    fig = px.bar(top, x="Country", y="Population", color="Country",
                 text_auto=True, title=f"Top Population — {continent}, {year}")
    fig.update_layout(paper_bgcolor="#f5f7fb")
    return fig

@app.callback(
    Output("bar_gdp", "figure"),
    [Input("continent", "value"), Input("year", "value")],
)
def update_bar_gdp(continent, year):
    filtered = df[(df["Continent"] == continent) & (df["Year"] == year)]
    top = filtered.sort_values("GDP per Capita", ascending=False).head(15)
    fig = px.bar(top, x="Country", y="GDP per Capita", color="Country",
                 text_auto=True, title=f"Top GDP per Capita — {continent}, {year}")
    fig.update_layout(paper_bgcolor="#f5f7fb")
    return fig

# ---- Run (use Render's PORT) ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
