"""
Django views
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import JSONUploadForm
from .services import parse, plot
from .services.algorithms import SimulatedAnnealing


def index(request: HttpRequest) -> HttpResponse:
    """
    Index page logic.
    """

    graph = None

    if request.method == "POST":
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["json_file"]

            target_objects, other_objects = parse.parse(file)
            tags = SimulatedAnnealing().run(target_objects, other_objects)
            graph = plot.get_plot_div(tags, other_objects)
    else:
        form = JSONUploadForm()

    return render(request, "index.html", {"form": form, "graph": graph})
