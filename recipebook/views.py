from django.shortcuts import render

from .models import Author, Recipe
from recipebook.forms import AddRecipeForm, AddAuthorForm
from django.contrib.auth.models import User


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


def recipeadd(request):
    html = "recipeadd.html"
    form = None
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data["title"],
                author=data["author"],
                description=data["description"],
                time_required=data["time_required"],
                instructions=data["instructions"],
            )
            return render(request, "thanks.html")
    else:
        form = AddRecipeForm()

    return render(request, html, {"form": form})


def authoradd(request):
    html = "authoradd.html"
    form = None
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data["name"],
                author_bio=data["author_bio"],
                user=User.objects.create_user(data["user"]),
            )
            return render(request, "thanks.html")
    else:
        form = AddAuthorForm()

    return render(request, html, {"form": form})

