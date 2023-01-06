from ast import literal_eval

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image


class PhonkData:
    """
    Class to generate the figures for the Phonk website
    """

    def __init__(self):
        self.df = pd.read_csv(
            "data_analysis/spotify_phonk.csv", encoding="utf-8"
        )

    def get_date_ranges_figures(self):

        df_date = self.df.copy()

        df_date = (
            df_date.groupby("date")
            .agg({"counter": sum, "streams": sum})
            .reset_index()
        )

        figure1 = go.Figure(
            go.Scatter(
                x=df_date["date"],
                y=df_date["counter"],
                name="Number of Tracks",
                line_color="#00D56C",
                fill="tozeroy",
            ),
            layout=go.Layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=go.layout.Margin(
                    l=0,  # left margin
                    r=0,  # right margin
                    b=0,  # bottom margin
                    t=30,  # top margin
                ),
                xaxis=dict(
                    gridcolor="gray",
                    color="white",
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    color="white",
                    showline=True,
                ),
            ),
        )

        figure2 = go.Figure(
            go.Scatter(
                x=df_date["date"],
                y=df_date["streams"],
                name="Number of Tracks",
                line_color="#F230AA",
                fill="tozeroy",
            ),
            layout=go.Layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    gridcolor="gray",
                    color="white",
                ),
                margin=go.layout.Margin(
                    l=0,  # left margin
                    r=0,  # right margin
                    b=0,  # bottom margin
                    t=30,  # top margin
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    color="white",
                    showline=True,
                ),
            ),
        )

        return figure1, figure2

    def get_best_artists(self):
        df_artist = self.df.copy()
        df_artist["artists"] = df_artist["artists"].apply(literal_eval)
        df_artist = (
            df_artist.explode("artists")
            .groupby("artists")
            .agg({"counter": sum, "streams": sum})
            .reset_index()
        )
        df_artist["artists"] = df_artist["artists"].astype(str)
        df_artist = df_artist.nlargest(10, "streams")
        df_artist

        trace_artist = go.Bar(
            x=df_artist["artists"],
            y=df_artist["streams"],
        )
        fig = go.Figure()
        fig.add_trace(trace_artist)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                showgrid=False, color="white", categoryorder="total ascending"
            ),
            margin=go.layout.Margin(
                l=0,  # left margin
                r=0,  # right margin
                b=0,  # bottom margin
                t=50,  # top margin
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                color="white",
                showline=True,
            ),
        )

        fig.update_traces(textfont=dict(color="white"), marker_color="#FF8DFD")

        return fig

    def get_explicit_content(self):
        df_explicit = self.df.copy()

        df_explicit = (
            df_explicit.groupby("explicit").agg({"counter": sum}).reset_index()
        )

        df_explicit["color"] = df_explicit.explicit.apply(
            lambda x: "#F230AA" if x else "#00D56C",
        ).astype("str")
        df_explicit["explicit"] = df_explicit.explicit.apply(
            lambda x: "explicit" if x else "not explicit",
        ).astype("str")

        return go.Figure(
            go.Pie(
                labels=df_explicit["explicit"],
                textinfo="label+percent",
                values=df_explicit["counter"],
                pull=[0, 0.2],
                marker_colors=df_explicit["color"],
            ),
            layout=go.Layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    gridcolor="gray",
                    color="white",
                ),
                margin=go.layout.Margin(
                    l=0,  # left margin
                    r=0,  # right margin
                    b=0,  # bottom margin
                    t=0,  # top margin
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    color="white",
                    showline=True,
                ),
            ),
        )

    def get_scatter_country(self):

        df_country = (
            self.df.copy()
            .groupby("country")
            .agg({"counter": sum, "streams": sum})
            .reset_index()
        )
        df_country = df_country.nlargest(10, "streams")
        df_country["country"] = df_country["country"].str.upper()
        df_country

        fig = px.scatter(
            df_country,
            x="counter",
            y="streams",
            hover_name="country",
            hover_data=["counter", "streams"],
        )
        fig.update_traces(marker_color="rgba(0,0,0,0)")

        minDim = df_country[["counter", "streams"]].max().idxmax()
        maxi = df_country[minDim].max()
        for i, row in df_country.iterrows():
            country_iso = row["country"]
            if country_iso != "GLOBAL":
                link_image = f"https://raw.githubusercontent.com/matahombres/CSS-Country-Flags-Rounded/master/flags/{country_iso}.png"
            else:
                link_image = Image.open("assets/img/GLOBAL.png")
            fig.add_layout_image(
                dict(
                    source=link_image,
                    xref="x",
                    yref="y",
                    xanchor="center",
                    yanchor="middle",
                    x=row["counter"],
                    y=row["streams"],
                    sizex=np.sqrt(row["streams"] / df_country["streams"].max())
                    * maxi
                    * 0.15
                    + maxi * 0.03,
                    sizey=np.sqrt(row["streams"] / df_country["streams"].max())
                    * maxi
                    * 0.15
                    + maxi * 0.03,
                    sizing="contain",
                    opacity=0.8,
                    layer="above",
                )
            )

        fig.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                showgrid=False,
                gridcolor="gray",
                color="white",
                showline=False,
                title="Number of tracks",
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                color="white",
                showline=False,
                title="Streams",
            ),
            height=350,
            margin=go.layout.Margin(
                l=0,  # left margin
                r=0,  # right margin
                b=0,  # bottom margin
                t=50,  # top margin
            ),
        )

        return fig
