from django.shortcuts import render, redirect

from .models import Author, Recipe
from recipebook.forms import AddRecipeForm, AddAuthorForm, SignupForm, LoginForm
from recipebook.helpers import can_user_edit_recipe, get_user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse
from django.http import HttpResponseRedirect


def index(request):
    html = "index.html"
    items = {"data": Recipe.objects.all()}
    return render(request, html, items)


def recipe_content(request, id):
    html = "content.html"
    recipes = Recipe.objects.filter(id=id)
    user = get_user(request)
    if user and recipes[0] in user.favorites.get_queryset():
        fav_unfav = "unheart"
    else:
        fav_unfav = "heart"
    user_can_edit = can_user_edit_recipe(request, recipes[0])
    recipe_list = {
        "recipes": recipes,
        "user_can_edit": user_can_edit,
        "fav_unfav": fav_unfav,
        "is_logged_in": bool(user)
        }
    return render(request, html, recipe_list)

@login_required
def toggle_favorite_recipe_view(request, recipe_id):
    user_id = request.user.author.id
    user = Author.objects.filter(id=user_id).first()
    recipe = Recipe.objects.filter(id=recipe_id).first()
    if recipe in user.favorites.get_queryset():
        user.favorites.remove(recipe)
    else:
        user.favorites.add(recipe)
    return redirect('/content/' + str(recipe_id))


def author(request, id):
    html = "author.html"
    items = {
        "data": Author.objects.filter(id=id),
        "recipes": Recipe.objects.filter(author_id=id),
    }
    return render(request, html, items)


@login_required()
def recipeadd(request):
    html = "recipeadd.html"
    form = None
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data["title"],
                # request.user.author will be user's name that has been authenticated
                author=request.user.author,
                description=data["description"],
                time_required=data["time_required"],
                instructions=data["instructions"],
            )
            return render(request, "thanks.html")
    else:
        form = AddRecipeForm()

    return render(request, html, {"form": form})


@login_required()
def recipeedit(request, recipeid):
    html = "recipeadd.html"
    form = None
    recipe = Recipe.objects.filter(id=recipeid)
    user_can_edit = can_user_edit_recipe(request,recipe[0])
    if not user_can_edit:
        return redirect('/') 
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.update(
                title=data["title"],
                description=data["description"],
                time_required=data["time_required"],
                instructions=data["instructions"]
            )
        return render(request, "recipeeditsuccess.html")
    else:
        recipe_instance = recipe.first()
        data = {
            "title": recipe_instance.title,
            "description": recipe_instance.description,
            "time_required": recipe_instance.time_required,
            "instructions": recipe_instance.instructions,
        }
        form = AddRecipeForm(initial=data)
    return render(request, html, {"form": form})


@staff_member_required()
def authoradd(request):
    html = "authoradd.html"
    form = None
    if request.user:
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
    else:
        login_view(request)

    return render(request, html, {"form": form})


def signup(request):
    html = "form.html"
    form = None
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                # Will go to the user model
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )
            login(request, user)
            # Author model
            Author.objects.create(name=data["name"], user=user)
            return HttpResponseRedirect(reverse("homepage"))
    else:
        form = SignupForm()
    return render(request, html, {"form": form})


def login_view(request):
    html = "form.html"
    form = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # authenticate returns true or false based on password, so we don't have to deal with hashing or handling the password
            # also returns instance of that user that just authenticated
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                login(request, user)
                # GET next drives the redirect when trying to login
                return HttpResponseRedirect(request.GET.get("next", "/"))
    else:
        form = LoginForm()
    return render(request, html, {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
