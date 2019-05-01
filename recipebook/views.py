from django.shortcuts import render

from .models import Author, Recipe


def index(request):
    html = "index.html"
    items = {"data": Recipe.objects.all()}
    return render(request, html, items)


def recipe_content(request, id):
    html = "content.html"
    recipe_list = {"recipes": Recipe.objects.filter(id=id)}
    return render(request, html, recipe_list)


def author(request, id):
    html = "author.html"
    items = {
        "data": Author.objects.filter(id=id),
        "recipes": Recipe.objects.filter(author_id=id),
    }
    return render(request, html, items)
