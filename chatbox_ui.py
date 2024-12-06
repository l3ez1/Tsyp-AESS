from dash import dcc, html, callback_context  # Import callback_context directly
from dash.dependencies import Input, Output, State
import requests

# Define the chatbox layout
def get_chatbox_layout():
    return html.Div(
        id="chatbox-wrapper",
        children=[
            # Icon on the left
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
                },
                children=[
                    html.Img(
                        src="https://cdn-icons-png.flaticon.com/512/4712/4712104.png",
                        style={"width": "40px", "height": "40px"}
                    )
                ],
            ),
            # Chatbox (hidden by default)
            html.Div(
                id="chatbox",
                style={
                    "position": "fixed",
                    "bottom": "100px",
                    "left": "30px",  # Align with the icon on the left
                    "width": "350px",
                    "borderRadius": "10px",
                    "backgroundColor": "#1e1e1e",
                    "padding": "15px",
                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.3)",
                    "display": "none",  # Initially hidden
                    "maxHeight": "400px",
                    "overflowY": "auto",
                },
                children=[
                    # Chatbox header
                    html.Div(
                        style={"borderBottom": "1px solid #333", "padding": "10px 0"},
                        children=[
                            html.Div(
                                style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                                children=[
                                    html.H4(
                                        "Chatbot Assistant",
                                        style={"color": "#00B8B8", "textAlign": "left", "margin": "0"},
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
                                            "margin": "0",
                                        },
                                    ),
                                ],
                            )
                        ],
                    ),
                    # Chat messages
                    html.Div(
                        id="chatDisplay",
                        style={
                            "flex": "1",
                            "overflowY": "auto",
                            "marginTop": "10px",
                            "maxHeight": "200px",  # Limit chatbox height
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
                    # User input and send button
                    html.Div(
                        style={"borderTop": "1px solid #333", "paddingTop": "10px", "display": "flex", "gap": "5px"},
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
                                    "backgroundColor": "#007BFF",
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
    )

# Define callback to toggle chatbox visibility
def register_callbacks(app):
    @app.callback(
        [
            Output("chatbox", "style"),
            Output("chatDisplay", "children"),
            Output("user-input", "value"),
        ],
        [
            Input("chat-icon", "n_clicks"),
            Input("send-button", "n_clicks"),
            Input("user-input", "n_submit"),
        ],
        [
            State("chatbox", "style"),
            State("user-input", "value"),
            State("chatDisplay", "children"),
            State("land-cover-dropdown", "value"),
            State("year-range-slider", "value"),
        ],
        prevent_initial_call=True,
    )
    def handle_chat_interaction(
        chat_icon_clicks, send_clicks, n_submit, current_style, user_query, chat_history, selected_land_cover, year_range
    ):
        ctx = callback_context  # Identify the triggering input
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

        # Ensure chat history is initialized
        if not chat_history:
            chat_history = []

        # Toggle chatbox visibility
        if triggered_id == "chat-icon":
            if current_style.get("display") == "none":
                return {**current_style, "display": "block"}, chat_history, None
            else:
                return {**current_style, "display": "none"}, chat_history, None

        # Handle chat input (Send button or Enter key)
        if triggered_id in ["send-button", "user-input"]:
            if not user_query:
                raise dash.exceptions.PreventUpdate

            # Append user query to chat history
            chat_history.append(
                html.Div(
                    user_query,
                    style={
                        "backgroundColor": "#007BFF",
                        "color": "white",
                        "borderRadius": "8px",
                        "padding": "10px",
                        "margin": "5px",
                        "alignSelf": "flex-end",
                        "maxWidth": "80%",
                    },
                )
            )

            # Call the Flask API
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={
                        "query": user_query,
                        "dashboard_data": {
                            "start_year": year_range[0],
                            "end_year": year_range[1],
                            "land_cover": selected_land_cover,
                        },
                    },
                )
                ai_response = response.json().get("response", "No response received from the AI.")
            except Exception as e:
                ai_response = f"Error contacting AI: {str(e)}"

            # Append AI response to chat history
            chat_history.append(
                html.Div(
                    ai_response,
                    style={
                        "backgroundColor": "#555",
                        "color": "white",
                        "borderRadius": "8px",
                        "padding": "10px",
                        "margin": "5px",
                        "alignSelf": "flex-start",
                        "maxWidth": "80%",
                    },
                )
            )

            # Clear the input field
            return current_style, chat_history, ""

        # Default case: Prevent updates
        raise dash.exceptions.PreventUpdate
