from recipebook.models import Author, Recipe


def can_user_edit_recipe(request, recipe):
    '''Determines if the logged in user has permission to edit a recipe.
    Only the original author or admin can edit recipes'''
    result = False
    if hasattr(request.user, 'author'):
        logged_in_user = Author.objects.filter(id=request.user.author.id).first()
        result = logged_in_user.id == recipe.author.id
    if request.user.is_staff:
        result = True
    return result