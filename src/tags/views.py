"""
Django views
"""

from django import http
from django.shortcuts import render

from .forms import JSONUploadForm
from .services import parse, plot
from .services.algorithms import SimulatedAnnealing


def index(request: http.HttpRequest) -> http.HttpResponse:
    """
    Index page logic.
    """

    graph = None

    if request.method == "POST":
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["json_file"]

            try:
                target_objects, other_objects = parse.parse(file)
            except (KeyError, ValueError):
                return http.HttpResponseBadRequest(
                    """Input JSON annotation contains errors.
                    Maybe some fields missing or values have wrong type."""
                )

            tags = SimulatedAnnealing().run(target_objects, other_objects)
            graph = plot.get_plot_div(tags, other_objects)
    else:
        form = JSONUploadForm()

    return render(request, "index.html", {"form": form, "graph": graph})
