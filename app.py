from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
# add near the top
import os
# ---- Data ----
df = px.data.gapminder().rename(columns={
    "country": "Country",
    "continent": "Continent",
    "year": "Year",
    "lifeExp": "Life Expectancy",
    "gdpPercap": "GDP per Capita",
    "pop": "Population",
    "iso_alpha": "ISO Alpha Country Code",
})

continents = sorted(df["Continent"].unique())
years = sorted(df["Year"].unique())

opt_continents = [{"label": c, "value": c} for c in continents]
opt_years = [{"label": y, "value": y} for y in years]

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"]
app = Dash(__name__, external_stylesheets=css)

# ---- Figure builders ----
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns), align="left"),
        cells=dict(values=[df[c] for c in df.columns], align="left"),
    )])
    fig.update_layout(paper_bgcolor="#e5ecf6", margin=dict(t=0, l=0, r=0, b=0), height=700)
    return fig

def create_population_chart(continent="Asia", year=1952):
    filtered = df[(df["Continent"] == continent) & (df["Year"] == year)]
    filtered = filtered.sort_values("Population", ascending=False).head(15)
    fig = px.bar(filtered, x="Country", y="Population", color="Country",
                 text_auto=True, title=f"Population — {continent}, {year}")
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_gdp_chart(continent="Asia", year=1952):
    filtered = df[(df["Continent"] == continent) & (df["Year"] == year)]
    filtered = filtered.sort_values("GDP per Capita", ascending=False).head(15)
    fig = px.bar(filtered, x="Country", y="GDP per Capita", color="Country",
                 text_auto=True, title=f"GDP per Capita — {continent}, {year}")
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_life_exp_chart(continent="Asia", year=1952):
    filtered = df[(df["Continent"] == continent) & (df["Year"] == year)]
    filtered = filtered.sort_values("Life Expectancy", ascending=False).head(15)
    fig = px.bar(filtered, x="Country", y="Life Expectancy", color="Country",
                 text_auto=True, title=f"Life Expectancy — {continent}, {year}")
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_choropleth_map(variable="Life Expectancy", year=1952):
    filtered = df[df["Year"] == year]
    fig = px.choropleth(
        filtered,
        locations="ISO Alpha Country Code",
        color=variable,
        hover_data=["Country", variable],
        color_continuous_scale="RdYlBu",
        title=f"{variable} Choropleth Map [{year}]",
    )
    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin=dict(l=0, r=0))
    return fig

# ---- Widgets ----
cont_population = dcc.Dropdown(id="cont_pop", options=opt_continents, value="Asia", clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=opt_years, value=1952, clearable=False)

cont_gdp = dcc.Dropdown(id="cont_gdp", options=opt_continents, value="Asia", clearable=False)
year_gdp = dcc.Dropdown(id="year_gdp", options=opt_years, value=1952, clearable=False)

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=opt_continents, value="Asia", clearable=False)
year_life_exp = dcc.Dropdown(id="year_life_exp", options=opt_years, value=1952, clearable=False)

year_map = dcc.Dropdown(id="year_map", options=opt_years, value=1952, clearable=False)
var_map = dcc.Dropdown(
    id="var_map",
    options=[{"label": x, "value": x} for x in ["Population", "GDP per Capita", "Life Expectancy"]],
    value="Life Expectancy",
    clearable=False,
)

# ---- Layout ----
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Gapminder Dataset Analysis", className="text-center fw-bold m-2"),
                html.Br(),
                dcc.Tabs(
                    [
                        dcc.Tab([html.Br(), dcc.Graph(id="dataset", figure=create_table())], label="Dataset"),
                        dcc.Tab(
                            [html.Br(), "Continent  ", cont_population, "  Year  ", year_population, html.Br(),
                             dcc.Graph(id="population")],
                            label="Population",
                        ),
                        dcc.Tab(
                            [html.Br(), "Continent  ", cont_gdp, "  Year  ", year_gdp, html.Br(),
                             dcc.Graph(id="gdp")],
                            label="GDP Per Capita",
                        ),
                        dcc.Tab(
                            [html.Br(), "Continent  ", cont_life_exp, "  Year  ", year_life_exp, html.Br(),
                             dcc.Graph(id="life_expectancy")],
                            label="Life Expectancy",
                        ),
                        dcc.Tab(
                            [html.Br(), "Variable  ", var_map, "  Year  ", year_map, html.Br(),
                             dcc.Graph(id="choropleth_map")],
                            label="Choropleth Map",
                        ),
                    ]
                ),
            ],
            className="col-8 mx-auto",
        ),
    ],
    style={"background-color": "#e5ecf6", "minHeight": "100vh"},
)

# ---- Callbacks ----
@app.callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value")])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@app.callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value")])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@app.callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value")])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@app.callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value")])
def update_map(variable, year):
    return create_choropleth_map(variable, year)

# ---- Run (Dash 3.x uses .run, not .run_server) ----
# ---- Run (use Render's PORT) ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
