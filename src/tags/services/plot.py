"""
Services for plotting logic
"""

import random
from typing import Sequence

import plotly
import plotly.graph_objects as go

from . import utils
from .geometry import Rectangle


def get_plot_div(
    tags: Sequence[Rectangle],
    other_objects: Sequence[Rectangle],
) -> str:
    r"""
    Add rectangle and inner text to plotly figure.

    Args:
        tags: List of tags.
        other_objects: List of objects that are not related to tags.

    Returns:
        plot_div: HTML \<div\> element with plot markup and logic.
    """

    fig = go.Figure()

    # Add tags and objects to figure
    for tag in tags:
        rect_color = random.randint(0, 0xFFFFFF)
        text_color = 0xFFFFFF - rect_color
        object_rect = tag.related

        add_rect(fig, object_rect, object_rect.label, rect_color, text_color)
        add_rect(fig, tag, "Tag", rect_color, text_color)

    # Add other objects to figure
    for other in other_objects:
        add_rect(fig, other, other.label, 0xAAAAAA, 0)

    # Fix figure axes range to fit all tags and objects
    s = [t.related for t in tags] + tags + other_objects
    objects_range = utils.get_bounding_rectangle(s)

    fig.update_xaxes(range=[objects_range.x0, objects_range.x1])
    fig.update_yaxes(range=[objects_range.y0, objects_range.y1])

    plot_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
    return plot_div


def add_rect(fig: go.Figure, rect: Rectangle, text: str, rect_color: int, text_color: int) -> None:
    """
    Add rectangle and inner text to plotly figure.

    Args:
        fig: plotly Figure.
        rect: Rectangle to add.
        text: Rectangle inner text.
        rect_color: Rectangle fill color.
        text_color: Text font color.
    """

    fig.add_shape(
        type="rect",
        x0=rect.x0,
        x1=rect.x1,
        y0=rect.y0,
        y1=rect.y1,
        fillcolor=f"#{rect_color:06x}",
    )

    fig.add_annotation(
        x=rect.center_x,
        y=rect.center_y,
        text=text,
        font={"color": f"#{text_color:06x}"},
        showarrow=False,
    )
