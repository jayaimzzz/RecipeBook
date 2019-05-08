from django.shortcuts import render

from .models import Author, Recipe
from recipebook.forms import AddRecipeForm, AddAuthorForm, SignupForm, LoginForm

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
    recipe_list = {"recipes": Recipe.objects.filter(id=id)}
    return render(request, html, recipe_list)


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
