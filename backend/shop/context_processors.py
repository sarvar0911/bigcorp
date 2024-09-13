from .models import Category


def categories(request):
    """
    This function retrieves all top-level categories from the database and 
    returns them as a dictionary under the key 'categories'.
    
    Args:
        request (HttpRequest): The HTTP request object. Unused in this context.
    
    Returns:
        dict: A dictionary with one key, 'categories', containing all top-level 
        categories.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
