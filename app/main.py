# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from data_analysis.data_analysis import PhonkData
from src.wikipedia import get_def

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def get_figure_and_title(title_figure, figure_plot):
    """
    get the title and the figure

    :param title_figure: (str), title of figure
    :param figure_plot: (dash figure), figure
    :return: (dash)
    """
    # Figure 1
    title = html.H5(
        title_figure,
        style={
            "margin": "0px",
            "padding-top": "10px",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "font-family": "“Segoe”, sans-serif",
        },
    )

    figure = dcc.Graph(
        figure=figure_plot,
        style={
            "margin-top": "0px",
            "height": "350px",
        },
    )

    return title, figure


def get_header():
    """
    get header

    :return: (dash)
    """
    # Header
    return html.H1(
        "PHONK Data analysis",
        style={
            "padding-top": "90px",
            "padding-left": "20px",
            "font-family": "“Segoe”, sans-serif",
            "height": "150px",
            "background-image": "url(assets/img/background.jpeg)",
        },
    )


def get_phonk_description():
    """
    get phonk description

    :return: (tuple)
    """
    # Title Genra description
    title = html.H5(
        "Genra description:",
        style={
            "padding-top": "60px",
            "color": "#00D56C",
        },
    )
    # The description got from Wikipedia
    p_element = html.P(
        get_def("Phonk"),
        style={
            "font-family": "“Segoe”, sans-serif",
            "color": "white",
            "text-align": "justify",
        },
    )

    return title, p_element


def get_logo():
    """
    get the logo

    :return: (Div)
    """
    return html.Div(
        [
            # Spotify Lgo
            html.Img(
                src="assets/img/spotify_logo.png",
                style={
                    "padding-bottom": "50px",
                    "textAlign": "center",
                },
            ),
        ],
        style={"textAlign": "center"},
    )


def main_app():
    """
    main Phonk analysis dashboard

    :return: (app)
    """
    df_phonk = PhonkData()
    figure1, figure2 = df_phonk.get_date_ranges_figures()
    app.layout = html.Div(
        children=[
            dbc.Row(
                [
                    # Side bar
                    dbc.Col(
                        [
                            get_logo(),
                            *get_phonk_description(),
                        ]
                    ),
                    # Right bar
                    dbc.Col(
                        [
                            # Header
                            get_header(),
                            # Container of plots
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            *get_figure_and_title(
                                                "Count of Phonk Tracks over the years",
                                                figure1,
                                            ),
                                            *get_figure_and_title(
                                                "Streams of Phonk tracks over the years",
                                                figure2,
                                            ),
                                        ],
                                        width=7,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Row(
                                                [
                                                    *get_figure_and_title(
                                                        "Top 10 stream countries scatter plot",
                                                        df_phonk.get_scatter_country(),
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    *get_figure_and_title(
                                                        "Explicit content percentage",
                                                        df_phonk.get_explicit_content(),
                                                    ),
                                                ]
                                            ),
                                        ],
                                        width=5,
                                    ),
                                ]
                            ),
                        ],
                        width=10,
                    ),
                ]
            )
        ],
    )

    return app


if __name__ == "__main__":
    app = main_app()
    app.run_server(debug=False, use_reloader=False, port=8000, host="0.0.0.0")
