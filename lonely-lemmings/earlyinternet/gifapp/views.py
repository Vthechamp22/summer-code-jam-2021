from django.shortcuts import render


def paint(request):
    return render(request, "draw.html")

def gallery(request):
    return render(request, "gallery.html")