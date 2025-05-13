import json

import plotly
import plotly.graph_objects
from django.shortcuts import render

from .forms import JSONUploadForm


def index(request):
    graph_div = None

    if request.method == "POST":
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["json_file"]
            data = json.load(file)

            fig = plotly.graph_objects.Figure()

            for obj in data:
                coordinates = obj["coordinates"]
                min_coordinates = coordinates["min"]
                max_coordinates = coordinates["max"]

                min_x = min_coordinates["x"]
                min_y = min_coordinates["y"]
                max_x = max_coordinates["x"]
                max_y = max_coordinates["y"]

                fig.add_shape(type="rect", x0=min_x, x1=max_x, y0=min_y, y1=max_y)

            graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
    else:
        form = JSONUploadForm()

    return render(request, "index.html", {"form": form, "graph": graph_div})
