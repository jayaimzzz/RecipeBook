# Introduction to Django: RecipeBook!

Application that serves recipes from different authors

An index page that lists all titles of the loaded recipes (they don't have to be real recipes; just fill them with lorem ipsum and some numbers.)
Each title is a link that takes you to a single page with the content of that recipe.
Each detail view for a recipe has the author name.
Clicking on the author's name should take you to an Author Detail page, where you can see a list of all the recipes that Author has contributed to.
Make all of the models accessible by the Admin only.

So we have three types of pages: a simple list view, a recipe detail view, and an author detail view. The admin panel will handle the creation views, so we don't need to worry too much about that.

Important Info:

Python 3.7, latest version of Django (2.1.2 as of this writing)
Start a project with `django-admin startproject {project name}` (for example, `django-admin startproject recipebook`)
Start the server with `python manage.py runserver`
After you create your models, run `python manage.py makemigrations {foldername}` (where foldername is the top level folder for your project) to create them, then `python manage.py migrate` to push them to the db. If you get stuck, delete the db and run the command again
If you change your models after running the migrations, run makemigrations and migrate again. If the migrations require the creation of a new table, django will attempt to automatically handle it; if things to weird, `python manage.py migrate --run-syncdb` is your friend
Create an admin user by running `python manage.py createsuperuser`
Don't go crazy on the front end. The goal is to just handle the database interactions and basic view path
Make sure that every detail page (author and recipe) has its own unique URL. If you reload the URL, the same page should appear -- no modals or manipulating the current information on the page. That's too complicated for what we're trying to achieve.
REITERATING: There are no extra points for pretty HTML! Don't spend time making everything on the front end look gorgeous; we just want to make sure we're serving the right information.

Author model:
Name
User backend (OnetoOne relationship against the Django user)
Brief Bio section (`TextField`)

Recipe Model:
Title
Author (ForeignKey)
Description
Time Required
Instructions (`TextField`)
