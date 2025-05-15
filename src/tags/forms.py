"""
Django forms for application
"""

from django import forms


class JSONUploadForm(forms.Form):
    """
    Form for JSON file upload.
    """

    json_file = forms.FileField(label=False)
