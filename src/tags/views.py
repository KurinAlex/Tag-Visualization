import json

from django.shortcuts import render

from .forms import JSONUploadForm


def index(request):
    rectangles = []
    if request.method == "POST":
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["json_file"]
            data = json.load(file)

            for obj in data:
                min_x = obj["coordinates"]["min"]["x"]
                min_y = obj["coordinates"]["min"]["y"]
                max_x = obj["coordinates"]["max"]["x"]
                max_y = obj["coordinates"]["max"]["y"]

                rectangles.append(
                    {
                        "x": min_x,
                        "y": min_y,
                        "width": max_x - min_x,
                        "height": max_y - min_y,
                        "label": obj["coordinates"]["family_name"],
                    }
                )
    else:
        form = JSONUploadForm()

    return render(request, "index.html", {"form": form, "rectangles": rectangles})
