import json
import random

import plotly
import plotly.graph_objects as go
from django.shortcuts import render

from . import utils
from .algorithms import SimulatedAnnealing
from .forms import JSONUploadForm
from .geometry import Rectangle


def index(request):
    graph = None

    if request.method == "POST":
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["json_file"]
            data = json.load(file)

            fig = create_graph(data)
            graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
    else:
        form = JSONUploadForm()

    return render(request, "index.html", {"form": form, "graph": graph})


def create_graph(data) -> go.Figure:
    fig = go.Figure()

    objects = []
    other = []
    tags = []

    for obj in data:
        tag = obj["document"]
        coordinates = obj["coordinates"]

        min_coordinates = coordinates["min"]
        max_coordinates = coordinates["max"]

        min_x = min_coordinates["x"]
        min_y = min_coordinates["y"]
        max_x = max_coordinates["x"]
        max_y = max_coordinates["y"]

        object_rectangle = Rectangle(x0=min_x, x1=max_x, y0=min_y, y1=max_y)

        if coordinates["family_name"] == "KIT(DS)1":
            objects.append(object_rectangle)
        else:
            other.append(object_rectangle)

    tags = SimulatedAnnealing().run(objects, other, 1.3, 2.8)
    for tag in tags:
        color = f"#{random.randint(0,0xFFFFFF):06x}"

        object_rect = tag.related
        fig.add_shape(
            type="rect",
            x0=object_rect.x0,
            x1=object_rect.x1,
            y0=object_rect.y0,
            y1=object_rect.y1,
            fillcolor=color,
            line={"color": "black"},
        )

        fig.add_shape(
            type="rect",
            x0=tag.x0,
            x1=tag.x1,
            y0=tag.y0,
            y1=tag.y1,
            fillcolor=color,
            line={"color": "black"},
        )

    for o in other:
        fig.add_shape(
            type="rect",
            x0=o.x0,
            x1=o.x1,
            y0=o.y0,
            y1=o.y1,
            fillcolor="#AAAAAA",
            line={"color": "black"},
        )

    s = objects + tags + other
    objects_range = utils.get_bounding_rectangle(s)

    fig.update_xaxes(range=[objects_range.x0, objects_range.x1])
    fig.update_yaxes(range=[objects_range.y0, objects_range.y1])

    return fig
