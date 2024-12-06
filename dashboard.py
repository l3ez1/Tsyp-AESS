import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from chatbox_ui import get_chatbox_layout, register_callbacks  # Import chatbox layout and callbacks
import requests


# Load the combined data (2001–2033)
df_combined = pd.read_csv("combined_land_cover_data.csv")

# Initialize Dash app with Bootstrap for better aesthetics
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
# Define styles for cards and elements
card_style = {
    "margin": "10px",
    "padding": "15px",
    "borderRadius": "5px",
    "boxShadow": "0px 4px 6px rgba(18, 22, 33, .12)",
}

title_style = {
    "textAlign": "center",
    "marginBottom": "20px",
    "color": "white",
    "fontWeight": "bold"
}

# App layout with enhanced UI/UX
app.layout = html.Div(
    style={"backgroundColor": "#000000", "color": "white", "padding": "20px"},
    children=[
        # Loading Screen (appears initially for 3-4 sec)
        html.Div(
            id="loading-screen",
            style={
                "position": "absolute",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "backgroundColor": "black",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            },
            children=[
                html.Iframe(
                    src='/assets/loading.html',  # Add your loading HTML file
                    style={'border': 'none', 'height': "100vh", 'width': "100vw", "overflow": "hidden",}
                )
            ]
        ),
        # Main Dashboard Content (Initially hidden)
        html.Div(
            id="dashboard-content",
            style={"display": "none"},  # Hidden until loading screen finishes
            children=[
                # Light/Dark theme toggle with professional emojis
                html.Div(
                    style={"position": "absolute", "top": "10px", "left": "20px"},
                    children=[
                        daq.ToggleSwitch(
                            id="theme-toggle",
                            label="Switch Theme",
                            labelPosition="bottom",
                            value=True,  # Dark mode by default
                        ),
                    ]
                ),
                html.H1(
                    "Land Cover Dashboard",
                    style={**title_style, "color": "#00B8B8"},  # Teal color for title
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4("Total Area", style={"color": "white", "fontWeight": "bold"}),
                                    html.H2("N/A", id="total-area"),
                                ],
                                style={**card_style, "fontSize": "30px"},
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4("Max Change", style={"color": "white", "fontWeight": "bold"}),
                                    html.H2("N/A", id="max-change"),
                                ],
                                style={**card_style, "fontSize": "30px"},
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4("Avg Annual Change", style={"color": "white", "fontWeight": "bold"}),
                                    html.H2("N/A", id="avg-change"),
                                ],
                                style={**card_style, "fontSize": "30px"},
                            )
                        ),
                    ]
                ),
                # Year Range Slider
                html.Div(
                    [
                        html.Label("Select Year Range:", style={"marginBottom": "10px"}),
                        dcc.RangeSlider(
                            id="year-range-slider",
                            min=2001,
                            max=2033,
                            step=1,
                            marks={year: str(year) for year in range(2001, 2034, 1)},
                            value=[2001, 2020],  # Default range value
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"textAlign": "center", "marginTop": "30px"},
                ),
                html.Div(
                    [
                        html.Label("Select a Land Cover Type:", style={"marginBottom": "10px"}),
                        dcc.Dropdown(
                            id="land-cover-dropdown",
                            options=[
                                {"label": land_cover, "value": land_cover}
                                for land_cover in df_combined["Land_Cover_Type"].unique()
                            ],
                            value=df_combined["Land_Cover_Type"].unique()[0],  # Default selection
                            style={"width": "50%", "marginBottom": "20px", "margin": "auto", "color": "black", "fontWeight": "bold"},
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
                html.Div(
                    [
                        html.H2("Yearly Trend", style={"textAlign": "center", "marginBottom": "10px"}),
                        dcc.Graph(id="trend-line"),
                        html.H2("Bar Chart", style={"textAlign": "center", "marginTop": "30px"}),
                        dcc.Graph(id="bar-chart"),
                        html.H2("Scatter Plot", style={"textAlign": "center", "marginTop": "30px"}),
                        dcc.Graph(id="scatter-plot"),
                        html.H2("Map Visualization", style={"textAlign": "center", "marginTop": "30px"}),
                        dcc.Graph(id="map-visualization"),
                    ],
                    style={"padding": "20px"},
                ),
                # Add the Chatbox layout
                # Add the Chatbox layout
                html.Div(
                    id="chatbox-wrapper",
                    children=[
                        # Chat Icon
                        html.Div(
                            id="chat-icon",
                            style={
                                "position": "fixed",
                                "bottom": "30px",
                                "left": "30px",  # Moved to the left
                                "backgroundColor": "#00B8B8",
                                "borderRadius": "50%",
                                "width": "60px",
                                "height": "60px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "cursor": "pointer",
                                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.3)",
                            },
                            children=[
                                html.Img(
                                    src="https://cdn-icons-png.flaticon.com/512/4712/4712104.png",
                                    style={"width": "40px", "height": "40px"},
                                )
                            ],
                        ),
                        # Chatbox
                        html.Div(
                            id="chatbox",
                            style={
                                "position": "fixed",
                                "bottom": "100px",
                                "left": "30px",  # Align with icon on the left
                                "width": "350px",
                                "borderRadius": "10px",
                                "backgroundColor": "#1e1e1e",
                                "padding": "15px",
                                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.3)",
                                "display": "none",  # Initially hidden
                                "maxHeight": "400px",
                                "overflowY": "auto",
                                "fontFamily": "Arial, sans-serif",
                            },
                            children=[
                                # Chat Header
                                html.Div(
                                    style={
                                        "borderBottom": "1px solid #333",
                                        "paddingBottom": "10px",
                                        "marginBottom": "10px",
                                    },
                                    children=[
                                        html.H4(
                                            "Chatbot Assistant",
                                            style={
                                                "color": "#00B8B8",
                                                "textAlign": "center",
                                            },
                                        ),
                                        html.Div(
                                            "Online",
                                            style={
                                                "backgroundColor": "green",
                                                "color": "white",
                                                "borderRadius": "15px",
                                                "padding": "5px 10px",
                                                "fontSize": "12px",
                                                "textAlign": "center",
                                                "width": "70px",
                                                "margin": "0 auto",
                                            },
                                        ),
                                    ],
                                ),
                                # Chat Display
                                html.Div(
                                    id="chatDisplay",
                                    style={
                                        "flex": "1",
                                        "overflowY": "auto",
                                        "marginBottom": "10px",
                                        "backgroundColor": "#1e1e1e",
                                        "padding": "10px",
                                        "borderRadius": "5px",
                                        "maxHeight": "200px",  # Scrollable height
                                        "border": "1px solid #00B8B8",
                                    },
                                    children=[
                                        html.Div(
                                            "Hello! How can I assist you today?",
                                            style={
                                                "backgroundColor": "#007BFF",
                                                "color": "white",
                                                "borderRadius": "8px",
                                                "padding": "10px",
                                                "margin": "5px",
                                                "alignSelf": "flex-end",
                                                "maxWidth": "80%",
                                            },
                                        ),
                                    ],
                                ),
                                # User Input and Send Button
                                html.Div(
                                    style={
                                        "borderTop": "1px solid #333",
                                        "paddingTop": "10px",
                                        "display": "flex",
                                        "gap": "5px",
                                    },
                                    children=[
                                        dcc.Input(
                                            id="user-input",
                                            placeholder="Type your message...",
                                            style={
                                                "flex": "1",
                                                "height": "40px",
                                                "padding": "5px",
                                                "borderRadius": "5px",
                                                "backgroundColor": "#333",
                                                "color": "white",
                                                "border": "1px solid #00B8B8",
                                            },
                                        ),
                                        html.Button(
                                            "Send",
                                            id="send-button",
                                            style={
                                                "height": "40px",
                                                "width": "70px",
                                                "backgroundColor": "#00B8B8",
                                                "color": "white",
                                                "borderRadius": "5px",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

            ],
        ),
        # Loading Spinner (Displays a spinner while loading)
        dcc.Loading(
            id="loading",
            type="circle",
            children=[html.Div(id="loading-output")]
        ),
        # Interval for triggering transition after delay
        dcc.Interval(
            id='loading-interval',
            interval=4000,  # 4 seconds delay
            n_intervals=0,
        ),
    ]
)

# Callback to update all graphs and metrics
@app.callback(
    [
        Output("trend-line", "figure"),
        Output("bar-chart", "figure"),
        Output("scatter-plot", "figure"),
        Output("map-visualization", "figure"),
        Output("total-area", "children"),
        Output("max-change", "children"),
        Output("avg-change", "children"),
        Output("loading-output", "children"),
        Output("loading-screen", "style"),
        Output("dashboard-content", "style"),
    ],
    [
        Input("land-cover-dropdown", "value"),
        Input("year-range-slider", "value"),
        Input("theme-toggle", "value"),
        Input("loading-interval", "n_intervals"),
    ],
)
def update_graphs(selected_land_cover, selected_year_range, is_dark_mode, n_intervals):
    # Show the dashboard after 4 seconds
    if n_intervals > 0:
        loading_screen_style = {"display": "none"}  # Hide the loading screen
        dashboard_content_style = {"display": "block"}  # Show the dashboard content
    else:
        loading_screen_style = {"display": "flex"}  # Show the loading screen
        dashboard_content_style = {"display": "none"}  # Hide the dashboard content

    start_year, end_year = selected_year_range
    filtered_df = df_combined[
        (df_combined["Land_Cover_Type"] == selected_land_cover)
        & (df_combined["Year"] >= start_year)
        & (df_combined["Year"] <= end_year)
    ]

    # Calculate metrics
    total_area = filtered_df["Value"].sum()
    max_change = filtered_df["Value"].max() - filtered_df["Value"].min()
    avg_change = filtered_df["Value"].diff().mean()

    # Format metrics
    total_area_text = f"{total_area:,.0f} sq. km"
    max_change_text = f"{max_change:+,.0f} sq. km"
    avg_change_text = f"{avg_change:+,.0f} sq. km/year"

    # Yearly Trend (Line Graph)
    trend_fig = px.line(
        filtered_df,
        x="Year",
        y="Value",
        title=f"Yearly Trend for {selected_land_cover}",
        labels={"Value": "Area (sq. km)"},
        template="plotly_dark" if is_dark_mode else "plotly",
        line_shape="spline",
    )

    # Bar Chart (Updated Color)
    bar_fig = px.bar(
        filtered_df,
        x="Year",
        y="Value",
        title=f"Bar Chart for {selected_land_cover}",
        labels={"Value": "Area (sq. km)"},
        template="plotly_dark" if is_dark_mode else "plotly",
        color="Value",  # Color bars by Value
        color_continuous_scale="Blues",  # Updated to a more appealing color
    )

    # Scatter Plot (Updated Color)
    scatter_fig = px.scatter(
        filtered_df,
        x="Year",
        y="Value",
        title=f"Scatter Plot for {selected_land_cover}",
        labels={"Value": "Area (sq. km)"},
        template="plotly_dark" if is_dark_mode else "plotly",
        size=filtered_df["Value"].abs(),
        color="Value",  # Color points by Value
        color_continuous_scale="Viridis",  # Updated to a professional color
    )

    # Map Visualization (Colorful markers)
    map_fig = px.scatter_geo(
        filtered_df,
        lat=[34.0] * len(filtered_df),  # Example latitude for Tunisia
        lon=[10.0] * len(filtered_df),  # Example longitude for Tunisia
        size=filtered_df["Value"].abs(),  # Use absolute values for size
        title=f"Map Visualization for {selected_land_cover}",
        template="plotly_dark" if is_dark_mode else "plotly",
        locationmode="ISO-3",
        hover_name="Year",
        color="Value",
        color_continuous_scale="Viridis",
    )

    return (
        trend_fig,
        bar_fig,
        scatter_fig,
        map_fig,
        total_area_text,
        max_change_text,
        avg_change_text,
        "Data Loaded Successfully!",  # This is the text that appears in the loading screen
        loading_screen_style,  # Hide the loading screen
        dashboard_content_style,  # Show the dashboard content
    )
from dash import callback_context
# Register the chatbox callbacks
try:
    register_callbacks(app)
except Exception as e:
    print(f"Error registering callbacks: {e}")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
