"""
This file contains the views for the job_hunters app.
"""

from django.shortcuts import render

# Create your views here.


def index(request):
    """
    View for the index page.
    """
    return render(request, "index.html")
