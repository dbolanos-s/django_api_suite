import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    try:
        response = requests.get(settings.API_URL, timeout=10)
        posts = response.json()
    except requests.RequestException:
        posts = []

    total_responses = len(posts)
    context = {
        "title": "Landing Page Dashboard",
        "total_responses": total_responses,
        "posts": posts[:10],
    }
    return render(request, "dashboard/index.html", context)
